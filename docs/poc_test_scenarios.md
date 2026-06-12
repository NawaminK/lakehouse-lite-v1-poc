# Lakehouse Lite v1 POC - Test Scenarios

> Quick navigation: use `docs/scenarios/index.md` for per-scenario pages. This file remains the full narrative reference. Scenario order and automation live in `scenarios.json`.

เอกสารนี้เพิ่มชุด **POC test scenarios** สำหรับทดสอบ Lakehouse Lite v1 บน Ubuntu 24.04 + Docker + MinIO + Iceberg + Spark + Trino + Superset + Airflow โดยตั้งใจให้ครอบคลุมมุมมองที่มักใช้ประเมิน data platform จริง ได้แก่ ingestion, transformation, data quality, schema evolution, CDC/upsert, time travel, partitioning, metadata, SQL serving, orchestration, BI, observability และ failure/recovery เบื้องต้น

> Scope นี้ยังเป็น local POC เครื่องเดียว ไม่ใช่ production architecture และยังไม่มี SSO, TLS, HA, fine-grained authorization, backup/restore, distributed object storage หรือ enterprise data catalog

---

## 1. วิธีรัน scenario ทั้งหมด

เริ่ม platform ก่อน

```bash
export AIRFLOW_UID=$(id -u)
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
docker compose up -d --build
docker compose ps
```

จากนั้นรันทุก scenario ผ่าน shell script

```bash
./scripts/run_all_scenarios.sh
```

หรือรันผ่าน Airflow UI

```text
URL: http://localhost:8081
DAG: lakehouse_v1_poc_scenarios
```

Airflow DAG จะรันลำดับหลักดังนี้

```text
base table creation
  -> base quality check
  -> schema evolution
  -> CDC merge/upsert
  -> time travel/snapshots
  -> partition/file layout
  -> expected quality failure
  -> Iceberg maintenance
  -> late arriving/backfill
  -> Trino SQL assertions
  -> Trino metadata inspection
```

---

## 2. Scenario inventory

| ID | Scenario | ประเด็นที่ทดสอบ | Component หลัก | Runnable |
|---:|---|---|---|---|
| 00 | Platform health check | container, port, service readiness | Docker, MinIO, Iceberg REST, Spark, Trino | manual |
| 01 | Base end-to-end lakehouse path | Spark เขียน Iceberg, Trino อ่าน, gold table | Spark, Iceberg, MinIO, Trino | yes |
| 02 | Base data quality gate | quality rules พื้นฐานก่อน publish | Spark | yes |
| 03 | Schema evolution | เพิ่ม column โดยไม่ rewrite old data | Spark, Iceberg | yes |
| 04 | CDC merge/upsert | insert/update/delete event เข้า current-state table | Spark, Iceberg MERGE | yes |
| 05 | Time travel and snapshots | อ่าน table version เก่าด้วย snapshot ID | Spark, Iceberg metadata | yes |
| 06 | Partitioning and file layout | hidden partitioning, files metadata | Spark, Iceberg metadata | yes |
| 07 | Expected data quality failure | ตรวจจับ bad records แบบตั้งใจให้ผิด | Spark | yes |
| 08 | Iceberg maintenance | snapshots/files growth และ expire snapshots | Spark, Iceberg procedures | yes |
| 09 | Late arriving data/backfill | late data แล้ว rebuild gold table | Spark, Iceberg | yes |
| 10 | Trino catalog discovery | SQL access, schema/table/column discovery | Trino, Iceberg | yes |
| 11 | Trino business queries | BI-style SQL query | Trino, Iceberg | yes |
| 12 | Trino assertions | SQL-level PASS/FAIL checks | Trino | yes |
| 13 | Metadata inspection | snapshots/history/files ผ่าน Trino | Trino, Iceberg metadata | yes |
| 14 | Superset dashboard validation | analyst consumption path | Superset, Trino | manual |
| 15 | MinIO physical object inspection | ดู metadata/data files จริง | MinIO | manual |
| 16 | Observability smoke test | container metrics และ service status | Prometheus, Grafana, cAdvisor | manual |
| 17 | Failure/recovery drill | stop/start service แล้วดู failure mode | Docker, Airflow, Spark, Trino | manual |

---

# Scenario 00 - Platform health check

## เป้าหมาย

ยืนยันว่า service หลักทั้งหมด start ได้ก่อนเริ่มทดสอบ data platform

## คำสั่ง

```bash
docker compose ps
```

ตรวจ URL หลัก

```text
MinIO Console: http://localhost:9001
Iceberg REST:  http://localhost:8181
Jupyter/Spark: http://localhost:8888
Trino:         http://localhost:8080
Superset:      http://localhost:8088
Airflow:       http://localhost:8081
Prometheus:    http://localhost:9090
Grafana:       http://localhost:3000
cAdvisor:      http://localhost:8090
```

## Expected result

- container หลักมีสถานะ `running` หรือ `healthy`
- MinIO login ได้ด้วย `admin/password`
- Trino CLI เรียกได้

```bash
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW CATALOGS"
```

ควรเห็น catalog อย่างน้อย

```text
iceberg
system
```

## สิ่งที่ต้องสังเกต

- ถ้า `minio` ไม่ healthy ให้ดู port 9000/9001 ชนกับ process อื่นหรือไม่
- ถ้า `trino` ไม่ขึ้น ให้ดูไฟล์ `trino/etc/catalog/iceberg.properties`
- ถ้า `airflow` เข้าไม่ได้ ให้ดู logs เพราะ `airflow standalone` อาจสร้าง password ใน log แม้เราตั้ง admin/admin ไว้แล้ว

---

# Scenario 01 - Base end-to-end lakehouse path

## เป้าหมาย

พิสูจน์เส้นทางหลักของ platform แบบ Databricks-lite:

```text
Spark -> Iceberg REST Catalog -> MinIO/S3 -> Trino -> BI/SQL
```

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py
```

## Script

```text
spark/jobs/01_create_tables.py
```

## สิ่งที่ script ทำ

1. สร้าง namespace

```text
lakehouse.bronze
lakehouse.silver
lakehouse.gold
```

2. สร้าง table

```text
lakehouse.bronze.orders_raw
lakehouse.silver.orders_clean
lakehouse.gold.daily_sales
```

3. เขียน sample orders เข้า bronze
4. transform เป็น silver โดยแปลง `order_date` เป็น `order_dt`
5. aggregate เป็น gold table `daily_sales`

## Expected result

ควรเห็น output ประมาณนี้

```text
Created Iceberg tables:
bronze.orders_raw
silver.orders_clean
gold.daily_sales
```

และเห็นข้อมูลใน gold table เช่น

```text
order_dt    province     net_sales  order_count
2026-06-01  Bangkok      1200.50    1
2026-06-01  Chiang Mai   550.00     1
2026-06-02  Bangkok     -200.00     1
2026-06-02  Phuket       880.75     1
2026-06-03  Bangkok      410.20     1
```

## Pass criteria

- Spark job จบด้วย exit code 0
- มี table ครบ bronze/silver/gold
- Trino query `iceberg.gold.daily_sales` ได้
- MinIO มี object ภายใต้ bucket `warehouse`

## Discussion point

Scenario นี้คือ happy path ขั้นต่ำของ lakehouse ถ้า scenario นี้ไม่ผ่าน ไม่ควรไปทดสอบ BI, governance หรือ ML ต่อ เพราะแปลว่า core storage/catalog/compute ยังไม่นิ่ง

---

# Scenario 02 - Base data quality gate

## เป้าหมาย

พิสูจน์ว่าก่อน publish data ไป downstream สามารถมี quality gate ขั้นต่ำได้

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/02_quality_check.py
```

## Script

```text
spark/jobs/02_quality_check.py
```

## Quality rules ที่เช็ก

| Rule | ความหมาย |
|---|---|
| `silver.orders_clean has rows` | table ต้องไม่ว่าง |
| `order_id is not null` | primary/business key ต้องไม่เป็น null |
| `amount is non-negative` | raw order amount ต้องไม่ติดลบ |
| `status is allowed` | status ต้องอยู่ใน `paid/refund` |

## Expected result

```text
PASS: silver.orders_clean has rows
PASS: order_id is not null
PASS: amount is non-negative in raw order records
PASS: status is allowed
```

## Pass criteria

- ทุก rule เป็น PASS
- script exit code 0

## Discussion point

ใน production ควรแยก data quality เป็นหลายระดับ เช่น schema contract, completeness, uniqueness, referential integrity, freshness, reconciliation, anomaly detection และ business rule validation

---

# Scenario 03 - Schema evolution

## เป้าหมาย

ทดสอบ capability สำคัญของ open table format คือเพิ่ม column ใหม่โดยไม่ต้อง rewrite data เก่าทั้งหมด

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/03_schema_evolution.py
```

## Script

```text
spark/jobs/scenarios/03_schema_evolution.py
```

## สิ่งที่ script ทำ

1. สร้าง table

```text
lakehouse.scenarios.orders_schema_evolution
```

2. insert records ด้วย schema แรก

```text
order_id, customer_id, order_dt, amount, status
```

3. ใช้ `ALTER TABLE ADD COLUMNS` เพื่อเพิ่ม column

```text
coupon_code, channel
```

4. insert records ใหม่ที่มี column ใหม่
5. query records ทั้งเก่าและใหม่
6. แสดง snapshot metadata

## Expected result

- old rows จะมี `coupon_code` และ `channel` เป็น `NULL`
- new rows จะมีค่าใน column ใหม่
- table schema หลัง alter จะมี column เพิ่ม
- metadata table `.snapshots` มีหลาย snapshot

## Pass criteria

- script exit code 0
- row count เท่ากับ 6
- old rows ยังอ่านได้หลังเพิ่ม column

## สิ่งที่ต้องสังเกต

Schema evolution ใน lakehouse ช่วยลด downtime แต่ไม่ได้แปลว่าสามารถเปลี่ยน schema แบบไม่มี governance ได้ ควรมี data contract และ backward/forward compatibility rule เช่น

```text
allowed: add nullable column
risky: rename column
risky: change data type
risky: drop column ที่ downstream ยังใช้อยู่
```

## คำถามสำหรับ vendor/internal team

- ถ้า schema เปลี่ยนจาก source system จะ detect และ approve อย่างไร
- table contract ใครเป็น owner
- downstream dashboard หรือ pipeline จะรู้ได้อย่างไรว่า schema เปลี่ยน

---

# Scenario 04 - CDC merge/upsert

## เป้าหมาย

ทดสอบ pattern สำหรับ current-state table หรือ dimension table ที่ต้องรับ insert/update/delete event

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/04_cdc_merge_upsert.py
```

## Script

```text
spark/jobs/scenarios/04_cdc_merge_upsert.py
```

## สิ่งที่ script ทำ

1. สร้าง table

```text
lakehouse.scenarios.customers_current
```

2. insert customer state เริ่มต้น
3. สร้าง temp view `customer_changes` ที่มี operation

```text
U = update
I = insert
D = delete
```

4. ใช้ `MERGE INTO` เพื่อ apply changes
5. ตรวจว่า active customers เหลือ 3 ราย

## Expected result

ตัวอย่างหลัง merge

```text
C001 -> tier เปลี่ยนจาก silver เป็น gold
C002 -> is_deleted = true
C003 -> full_name ถูก update
C004 -> customer ใหม่ถูก insert
```

## Pass criteria

- MERGE สำเร็จ
- active customer count = 3
- table มี snapshot ของ merge operation

## สิ่งที่ต้องสังเกต

CDC/upsert เป็น workload ที่ต้องระวังเรื่อง

```text
primary key uniqueness
event ordering
duplicate events
late events
delete semantics
merge performance
small files
compaction
```

## Discussion point

ใน production ต้องตัดสินใจว่า delete จะเป็น hard delete, soft delete หรือ SCD Type 2 และต้องมี rule สำหรับกรณี event มาช้า/มาซ้ำ

---

# Scenario 05 - Time travel and snapshots

## เป้าหมาย

ทดสอบความสามารถในการอ่าน table version เก่าผ่าน Iceberg snapshot ID

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/05_time_travel_snapshots.py
```

## Script

```text
spark/jobs/scenarios/05_time_travel_snapshots.py
```

## สิ่งที่ script ทำ

1. สร้าง table

```text
lakehouse.scenarios.account_balances_history
```

2. insert snapshot แรก 2 rows
3. อ่าน snapshot ID แรกจาก metadata table
4. insert เพิ่มอีก 2 rows
5. อ่าน current table ได้ 4 rows
6. อ่าน table ย้อนกลับด้วย `snapshot-id` แล้วได้ 2 rows

## Expected result

```text
current_count = 4
v1_count = 2
```

## Pass criteria

- query current table ได้ 4 rows
- query snapshot แรกได้ 2 rows
- script exit code 0

## สิ่งที่ต้องสังเกต

Time travel ช่วยเรื่อง audit, debugging, reconciliation, rollback analysis และ reproducibility แต่มี trade-off เรื่อง storage และ metadata growth จึงต้องมี snapshot retention policy

## Discussion point

ควรกำหนด retention policy เช่น

```text
bronze: retain snapshots 30-90 days
gold: retain snapshots 90-365 days
sandbox: retain snapshots 7-14 days
regulated datasets: ตาม policy/compliance
```

---

# Scenario 06 - Partitioning and file layout

## เป้าหมาย

ทดสอบ hidden partitioning และ metadata table สำหรับดู physical file layout

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/06_partition_file_layout.py
```

## Script

```text
spark/jobs/scenarios/06_partition_file_layout.py
```

## สิ่งที่ script ทำ

1. สร้าง table

```text
lakehouse.scenarios.orders_partitioned
```

2. partition table ด้วย

```text
days(order_ts), province
```

3. insert records หลายวัน/หลายจังหวัด
4. query metadata table `.files`
5. แสดง query plan ของ filter ตาม date/province

## Expected result

- table มี 5 rows
- metadata table `.files` แสดง `file_path`, `partition`, `record_count`, `file_size_in_bytes`
- query plan แสดง filter/predicate ที่ engine ใช้ได้

## Pass criteria

- script exit code 0
- query metadata files table ได้

## สิ่งที่ต้องสังเกต

Partitioning ไม่ควรเลือกจากความเคยชิน เช่น partition by date เสมอ แต่ควรเลือกจาก query pattern, cardinality, ingest pattern และ file size target

## Anti-pattern

```text
partition column cardinality สูงมาก เช่น customer_id แบบ millions
partition เล็กเกินไปจนเกิด small files จำนวนมาก
partition ตาม field ที่ query ไม่ค่อย filter
ไม่มี compaction job
```

---

# Scenario 07 - Expected data quality failure

## เป้าหมาย

ทดสอบว่าระบบสามารถจับ bad records ได้จริง ไม่ใช่มีแต่ happy path

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/07_quality_failure_expected.py
```

## Script

```text
spark/jobs/scenarios/07_quality_failure_expected.py
```

## ข้อมูลเสียที่ตั้งใจใส่เข้าไป

| Issue | ตัวอย่าง |
|---|---|
| duplicate key | `order_id = 3001` ซ้ำ |
| null key | `order_id IS NULL` |
| missing customer | `customer_id IS NULL` |
| negative amount | `amount = -10.00` |
| invalid status | `status = void` |

## Expected result

Scenario นี้จะถือว่า PASS เมื่อพบ violation ตามที่คาดไว้

```text
null_order_id: 1
null_customer_id: 1
negative_amount: 1
invalid_status: 1
duplicate_order_id_groups: 1
PASS: Scenario 07 completed. Quality gate detected the expected bad records.
```

## Pass criteria

- violation count ทุกตัวมากกว่า 0
- script exit code 0

## สิ่งที่ต้องสังเกต

Scenario นี้ไม่ได้ตั้งใจให้ pipeline fail ทั้ง DAG แต่ตั้งใจให้พิสูจน์ว่า validation logic จับข้อมูลเสียได้ ถ้าอยากจำลอง production failure จริง ให้เปลี่ยน script ให้ `raise RuntimeError` เมื่อเจอ violation แล้วดู Airflow task fail/alert

## Discussion point

ใน production ควรออกแบบ action เมื่อเจอ bad data เช่น

```text
fail pipeline
quarantine bad records
publish partial data with warning
notify owner
block downstream dashboard refresh
create incident ticket
```

---

# Scenario 08 - Iceberg maintenance

## เป้าหมาย

ทดสอบว่า table ที่มีหลาย write จะมี snapshot/file metadata เพิ่มขึ้น และแสดง pattern สำหรับ maintenance เช่น expire snapshots

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/08_iceberg_maintenance.py
```

## Script

```text
spark/jobs/scenarios/08_iceberg_maintenance.py
```

## สิ่งที่ script ทำ

1. สร้าง table

```text
lakehouse.scenarios.maintenance_demo
```

2. insert หลาย batch เพื่อสร้างหลาย snapshots
3. query จำนวน snapshots
4. query จำนวน data files
5. พยายามเรียก Iceberg procedure

```sql
CALL lakehouse.system.expire_snapshots(
  table => 'scenarios.maintenance_demo',
  older_than => TIMESTAMP '2099-01-01 00:00:00',
  retain_last => 1
)
```

6. query snapshot/file count หลัง maintenance attempt

## Expected result

- ก่อน maintenance จะเห็นหลาย snapshots
- หลัง maintenance อาจเห็น snapshot count ลดลง ถ้า image/catalog version รองรับ procedure ครบ
- ถ้า local image ไม่รองรับ procedure script จะไม่ทำให้ POC fail แต่จะ print reason และ SQL pattern ให้ดู

## Pass criteria

- script exit code 0
- metadata table query ได้
- เห็นเหตุผลว่าทำไมต้องมี maintenance job

## สิ่งที่ต้องสังเกต

Lakehouse production ต้องมี maintenance workflow เช่น

```text
expire snapshots
remove orphan files
rewrite/compact small files
rewrite manifests
compute table statistics
validate freshness
```

ถ้าไม่มี maintenance table จะ query ช้าลง metadata โตขึ้น และ object storage จะมีไฟล์ที่ไม่ได้ใช้งานสะสม

---

# Scenario 09 - Late arriving data and backfill rebuild

## เป้าหมาย

ทดสอบกรณีข้อมูลมาช้า และ gold aggregate ต้อง rebuild หรือ backfill ให้ deterministic

## คำสั่ง

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/scenarios/09_late_arriving_backfill.py
```

## Script

```text
spark/jobs/scenarios/09_late_arriving_backfill.py
```

## สิ่งที่ script ทำ

1. สร้าง bronze table

```text
lakehouse.scenarios.orders_backfill_raw
```

2. insert initial batch ของวันที่ 2026-06-10
3. build gold aggregate

```text
lakehouse.scenarios.daily_sales_backfill
```

4. append late batch ที่มีข้อมูลวันที่ 2026-06-09 และ refund ของวันที่ 2026-06-10
5. rebuild gold table ใหม่จาก bronze ทั้งหมด

## Expected result

ก่อน late data จะมี aggregate เฉพาะวันที่ 2026-06-10 หลัง rebuild จะมีวันที่ 2026-06-09 เพิ่ม และยอดของ Bangkok วันที่ 2026-06-10 จะถูกปรับจาก refund

ผลลัพธ์หลัง rebuild ควรมี 4 aggregate groups:

```text
2026-06-09 Bangkok  net_sales = 300.00, order_count = 1
2026-06-09 Phuket   net_sales = 40.00,  order_count = 1
2026-06-10 Bangkok  net_sales = 280.00, order_count = 3
2026-06-10 Phuket   net_sales = 50.00,  order_count = 1
```

เหตุผลที่เป็น 4 rows คือ gold table group by ด้วย `order_dt, province` และ late batch เพิ่มข้อมูลวันที่ 2026-06-09 ให้ทั้ง Bangkok และ Phuket

## Pass criteria

- gold aggregate หลัง rebuild มี 4 rows เพราะ aggregate ตาม `(order_dt, province)`
- script exit code 0
- snapshot ของ gold table แสดงการ create/replace

## สิ่งที่ต้องสังเกต

Late-arriving data เป็นเรื่องปกติของ real-world pipeline โดยเฉพาะธุรกรรม, IoT, log, payment, telecom และ external data feeds ดังนั้น pipeline ต้องรองรับ

```text
backfill by partition/date range
idempotent rerun
deduplication
watermark
reconciliation
SLA/freshness tracking
```

---

# Scenario 10 - Trino catalog discovery

## เป้าหมาย

ทดสอบว่า SQL engine เห็น catalog/schema/table/column ที่ Spark สร้างผ่าน Iceberg catalog เดียวกัน

## คำสั่ง

```bash
docker compose exec trino trino \
  --server http://localhost:8080 \
  --file /tmp/sql/scenarios/01_catalog_discovery.sql
```

## SQL file

```text
sql/scenarios/01_catalog_discovery.sql
```

## Expected result

ควรเห็น

```text
iceberg catalog
bronze/silver/gold/scenarios schemas
scenarios tables
columns ของ daily_sales และ orders_schema_evolution
```

## Pass criteria

- Trino query สำเร็จ
- เห็น table ที่ Spark สร้าง

## Discussion point

นี่คือ core benefit ของ open table format + shared catalog: หลาย engine เห็น table เดียวกันโดยไม่ต้อง copy data

---

# Scenario 11 - Trino business queries

## เป้าหมาย

ทดสอบ BI/analyst-style queries ผ่าน Trino

## คำสั่ง

```bash
docker compose exec trino trino \
  --server http://localhost:8080 \
  --file /tmp/sql/scenarios/02_business_queries.sql
```

## SQL file

```text
sql/scenarios/02_business_queries.sql
```

## Query examples

- daily sales by date/province
- total net sales by province
- backfill aggregate by date
- active customers by tier

## Pass criteria

- Query ทุกตัว return result
- ไม่มี error เรื่อง catalog/schema/table missing

## สิ่งที่ต้องสังเกต

ใน production ต้องทดสอบเพิ่มเรื่อง concurrency, query latency, BI dashboard refresh, workload isolation และ resource group/queue policy

---

# Scenario 12 - Trino SQL assertions

## เป้าหมาย

ใช้ SQL query เป็น smoke test หลังรัน scenario ทั้งหมด

## คำสั่ง

```bash
docker compose exec trino trino \
  --server http://localhost:8080 \
  --file /tmp/sql/scenarios/03_scenario_assertions.sql
```

## SQL file

```text
sql/scenarios/03_scenario_assertions.sql
```

## Expected result

ทุก row ควรเป็น `PASS`

```text
check_name                              result  actual
active customers after CDC merge = 3    PASS    3
backfill gold aggregate rows = 4        PASS    4
backfill total net_sales = 670.00       PASS    670.00
backfill Bangkok refund adjusted = 280.00 PASS  280.00, orders=3
maintenance demo rows = 10              PASS    10
partitioned table rows = 5              PASS    5
schema evolution row count = 6          PASS    6
time travel current table rows = 4      PASS    4
```

## Pass criteria

- ทุก assertion เป็น PASS

## สิ่งที่ต้องสังเกต

SQL assertion แบบนี้เหมาะกับ smoke test แต่ยังไม่แทน data quality framework เต็มรูปแบบ เพราะยังไม่มี severity, quarantine, expectation store, alerting, lineage integration หรือ history ของผล validation

---

# Scenario 13 - Iceberg metadata inspection through Trino

## เป้าหมาย

ทดสอบว่า Trino สามารถอ่าน Iceberg metadata tables ได้ เช่น snapshots, history และ files

## คำสั่ง

```bash
docker compose exec trino trino \
  --server http://localhost:8080 \
  --file /tmp/sql/scenarios/04_metadata_inspection.sql
```

## SQL file

```text
sql/scenarios/04_metadata_inspection.sql
```

## Metadata tables ที่ใช้

```text
<table>$snapshots
<table>$history
<table>$files
```

## Expected result

ควรเห็น

- snapshot IDs
- committed timestamp
- operation เช่น append, overwrite, replace
- data file paths
- record count ต่อ file

## Pass criteria

- metadata queries สำเร็จ
- เห็น snapshot และ file metadata ของ scenario tables

## Discussion point

Metadata inspection สำคัญสำหรับ debugging, audit, performance tuning และ incident analysis เช่น ตรวจว่า write operation ไหนทำให้ row count ผิด หรือ batch ไหนสร้าง small files มากผิดปกติ

---

# Scenario 14 - Superset dashboard validation

## เป้าหมาย

ทดสอบ consumption path สำหรับ analyst/BI user

## ขั้นตอน

เปิด Superset

```text
http://localhost:8088
username: admin
password: admin
```

เพิ่ม database connection

```text
trino://admin@trino:8080/iceberg/gold
```

สร้าง dataset จาก table

```text
daily_sales
```

สร้าง chart อย่างน้อย 2 แบบ

```text
1. Bar chart: net_sales by province
2. Time-series/table: net_sales by order_dt
```

ถ้าต้องการใช้ scenario schema ให้เพิ่ม connection อีกชุดหรือแก้ schema เป็น

```text
trino://admin@trino:8080/iceberg/scenarios
```

แล้วสร้าง dataset เช่น

```text
daily_sales_backfill
customers_current
orders_schema_evolution
```

## Expected result

- Superset connect Trino ได้
- เห็น dataset columns
- สร้าง chart ได้
- refresh chart ได้

## Pass criteria

- dashboard เปิดได้โดยไม่มี query error
- query วิ่งผ่าน Trino ไม่ใช่อ่านไฟล์จาก MinIO ตรง

## สิ่งที่ต้องสังเกต

Superset ใน POC นี้ยังไม่มี semantic layer, row-level security, SSO หรือ certified dataset workflow ดังนั้น production ต้องเพิ่ม governance layer ก่อนให้ business user ใช้จริง

---

# Scenario 15 - MinIO physical object inspection

## เป้าหมาย

ดูว่า Iceberg table จริง ๆ ถูกเก็บเป็น object/file อย่างไรบน S3-compatible storage

## ขั้นตอน

เปิด MinIO Console

```text
http://localhost:9001
username: admin
password: password
```

เข้า bucket

```text
warehouse
```

ดู path เช่น

```text
warehouse/bronze/orders_raw/
warehouse/silver/orders_clean/
warehouse/gold/daily_sales/
warehouse/scenarios/orders_schema_evolution/
warehouse/scenarios/orders_partitioned/
```

## สิ่งที่ควรเห็น

```text
data/
metadata/
```

ใน `metadata/` จะเห็น metadata json/manifest files ของ Iceberg

ใน `data/` จะเห็น data files เช่น Parquet

## Pass criteria

- มี object ภายใต้ bucket `warehouse`
- table ที่สร้างจาก Spark มี metadata/data files

## Discussion point

ห้ามให้ business users อ่าน path ใน object storage ตรง เพราะจะ bypass catalog, access control, audit, table semantics และ metadata consistency ควรให้ผ่าน Trino/Spark/catalog เท่านั้น

---

# Scenario 16 - Observability smoke test

## เป้าหมาย

ทดสอบว่าเรามองเห็น resource usage และ service health เบื้องต้นได้

## Prometheus

เปิด

```text
http://localhost:9090
```

ลอง query

```promql
up
```

หรือ container metrics จาก cAdvisor เช่น

```promql
container_memory_usage_bytes
container_cpu_usage_seconds_total
```

## Grafana

เปิด

```text
http://localhost:3000
username: admin
password: admin
```

เพิ่ม Prometheus data source

```text
http://prometheus:9090
```

สร้าง dashboard เบื้องต้นจาก metrics

```text
container CPU
container memory
container network I/O
container filesystem usage
```

## Pass criteria

- Prometheus scrape target ได้
- Grafana query Prometheus ได้
- เห็น resource usage ของ container หลัก

## สิ่งที่ต้องสังเกต

Observability ใน POC นี้ยังเป็น infrastructure-level เป็นหลัก ยังไม่ได้มี application-level metrics เช่น Spark job duration, Trino query latency, Airflow DAG SLA, Iceberg table freshness หรือ data quality history

---

# Scenario 17 - Failure/recovery drill

## เป้าหมาย

จำลอง failure เบื้องต้นเพื่อดู behavior ของ platform และ runbook ที่ควรมี

## 17.1 Trino unavailable

หยุด Trino

```bash
docker compose stop trino
```

ลองรัน SQL assertion

```bash
docker compose exec trino trino --server http://localhost:8080 --file /tmp/sql/scenarios/03_scenario_assertions.sql
```

Expected result

```text
command fails because trino container is stopped
```

กู้คืน

```bash
docker compose start trino
docker compose logs -f trino
```

ตรวจซ้ำ

```bash
docker compose exec trino trino --server http://localhost:8080 --execute "SHOW CATALOGS"
```

## 17.2 MinIO unavailable

หยุด MinIO

```bash
docker compose stop minio
```

ลอง Spark job

```bash
docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py
```

Expected result

```text
Spark/Iceberg write fails because object storage is unavailable
```

กู้คืน

```bash
docker compose start minio
docker compose logs -f minio
```

## 17.3 Data quality failure as pipeline blocker

แก้ script `07_quality_failure_expected.py` ให้ raise error เมื่อพบ violation แล้ว run ผ่าน Airflow เพื่อดู task fail

Conceptual production behavior

```text
bad data detected
  -> task fails
  -> downstream task blocked
  -> alert sent
  -> bad records quarantined
  -> data owner investigates
```

## Pass criteria

- failure mode เข้าใจได้
- service recovery ทำได้
- มี runbook ว่าต้องดู log ที่ไหนและแก้ไขอย่างไร

---

## 3. Recommended POC scoring rubric

ใช้ rubric นี้ให้ทีมประเมินหลังจบ POC

| Area | คำถามประเมิน | คะแนน 1-5 |
|---|---|---:|
| Core lakehouse | Spark เขียน Iceberg และ Trino อ่านได้เสถียรหรือไม่ |  |
| Storage | MinIO path/object layout เข้าใจและ monitor ได้หรือไม่ |  |
| Catalog | schema/table metadata ใช้งานข้าม engine ได้หรือไม่ |  |
| SQL serving | Trino query ง่าย เร็วพอ และต่อ BI ได้หรือไม่ |  |
| Data engineering | pipeline pattern bronze/silver/gold ชัดหรือไม่ |  |
| Data quality | จับ bad data ได้และมี action ที่ชัดเจนหรือไม่ |  |
| Schema evolution | รับ schema change ได้โดยไม่กระทบ downstream มากเกินไปหรือไม่ |  |
| CDC/upsert | merge pattern ใช้กับ data จริงได้หรือไม่ |  |
| Time travel | snapshot/history ช่วย debug/audit ได้จริงหรือไม่ |  |
| Maintenance | มี strategy จัดการ snapshots/small files หรือไม่ |  |
| Orchestration | Airflow คุม dependency/retry/log ได้พอหรือไม่ |  |
| BI | Superset/Trino ตอบโจทย์ analyst หรือไม่ |  |
| Observability | เห็น metrics/logs เพียงพอสำหรับ support หรือไม่ |  |
| Security readiness | มีช่องว่างด้าน identity/access/audit อะไรบ้าง |  |
| Operability | ทีมดูแลเองไหวหรือไม่เมื่อเทียบกับ managed platform |  |

คะแนนรวมไม่ได้มีไว้ตัดสินว่าใช้ได้หรือไม่ได้ทันที แต่มีไว้ระบุว่า area ไหนต้องเสริมก่อน production

---

## 4. สิ่งที่ควรเพิ่มหลัง POC นี้

ถ้า POC นี้ผ่านแล้ว รุ่นถัดไปควรเพิ่มตามลำดับนี้

```text
1. OpenMetadata หรือ DataHub สำหรับ data catalog, glossary, ownership, lineage
2. OpenLineage/Marquez สำหรับ pipeline lineage
3. Keycloak สำหรับ SSO
4. Trino access control หรือ Ranger/OPA integration
5. Secret management แทน hard-coded credentials
6. Distributed MinIO หรือ object storage จริง
7. Airflow production deployment แยก scheduler/webserver/worker/database
8. Spark job packaging ผ่าน Git/CI/CD
9. Data quality framework เช่น Great Expectations หรือ Soda Core
10. Table maintenance DAG รายวัน
11. Backup/restore drill
12. Dev/test/prod environment separation
```

---

## 5. คำสั่งล้างและเริ่มใหม่

หยุด platform แต่เก็บ volume

```bash
docker compose down
```

ล้างข้อมูลทั้งหมด

```bash
./scripts/reset_poc_data.sh
```

เริ่มใหม่

```bash
export AIRFLOW_UID=$(id -u)
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
docker compose up -d --build
./scripts/run_all_scenarios.sh
```
