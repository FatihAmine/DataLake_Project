from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, self.header_title, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, num, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(25, 60, 120)
        self.cell(0, 12, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(25, 60, 120)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def code_block(self, text):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(240, 240, 245)
        self.set_text_color(20, 20, 20)
        self.set_draw_color(200, 200, 210)
        lines = text.split("\n")
        block_h = max(len(lines) * 4.5, 5) + 4
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, self.w - 2 * self.l_margin, block_h, style="DF")
        self.set_xy(x + 3, y + 2)
        for line in lines:
            self.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")
            self.set_x(x + 3)
        self.ln(4)

    def bullet(self, text, indent=10):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(4, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def note_box(self, text):
        self.set_font("Helvetica", "I", 9)
        self.set_fill_color(255, 250, 230)
        self.set_draw_color(210, 180, 80)
        self.set_text_color(100, 80, 20)
        lines = text.split("\n")
        h = max(len(lines) * 5, 5) + 4
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, self.w - 2 * self.l_margin, h, style="DF")
        self.set_xy(x + 3, y + 2)
        for line in lines:
            self.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
            self.set_x(x + 3)
        self.ln(4)


CONTENT = {
    "en": {
        "header": "Data Lakehouse Project - Setup Guide",
        "title": "Data Lakehouse",
        "subtitle": "Project Setup & Completion Guide",
        "tagline": "Trino + Iceberg + ClickHouse + MinIO",
        "intro1": "This guide walks through everything needed to get the full stack running.",
        "intro2": "Both frontend UIs are already built. Focus is on infrastructure and data seeding.",
        "toc_title": "Table of Contents",
        "toc": [
            ("1", "Project Overview"),
            ("2", "Prerequisites"),
            ("3", "Quick Start - Docker Compose"),
            ("4", "Step 1: Fix MinIO Bucket Permissions"),
            ("5", "Step 2: Seed ClickHouse with Sample Data"),
            ("6", "Step 3: Seed Iceberg Tables via Trino"),
            ("7", "Step 4: Run the Frontend UIs"),
            ("8", "Port Reference"),
            ("9", "Architecture Diagram"),
            ("10", "Troubleshooting"),
            ("11", "Next Steps & Ideas"),
        ],
        "s1_title": "Project Overview",
        "s1_intro": "This is a modern data lakehouse platform that combines a data lake (MinIO / S3) with Apache Iceberg (for ACID transactions on the lake), Trino (for federated SQL queries across sources), and ClickHouse (for fast columnar analytics).",
        "s1_apps": "The project has two frontend applications:",
        "s1_app1": "data-product-ui -- A sales analytics dashboard showing revenue, units sold, sales per day, sales by category, and top products. Queries ClickHouse views in the ecommerce_product database.",
        "s1_app2": "query-explorer-ui -- A federated SQL query explorer with a catalog/schema/table browser and a CSV upload tool that ingests data into ClickHouse via S3.",
        "s1_note": "Both UIs are React + Vite apps. Source code, dependencies (node_modules), and production builds (dist/) are all present. No frontend coding is needed.",
        "s1_services_title": "Services",
        "s1_services": [
            "MinIO (ports 9000, 9001) -- S3-compatible object storage. Root bucket: warehouse",
            "PostgreSQL (port 5432) -- Stores Iceberg catalog metadata (database: iceberg_catalog)",
            "Trino (port 8080) -- Open-source distributed SQL query engine",
            "ClickHouse (port 8123) -- Columnar analytics database",
            "mc -- Init container that creates the warehouse bucket on MinIO at startup",
        ],
        "s2_title": "Prerequisites",
        "s2_intro": "Make sure you have the following installed before starting:",
        "s2_items": [
            "Docker Desktop (or Docker Engine + Docker Compose plugin)",
            "Node.js v18+ and npm (for running the frontend UIs outside Docker)",
            "A web browser (Chrome / Firefox / Edge)",
            "At least 8 GB of RAM allocated to Docker",
            "Git (optional, for version control)",
        ],
        "s2_check": "To verify Docker is ready, run:",
        "s2_code": "docker compose version\ndocker info",
        "s3_title": "Quick Start - Docker Compose",
        "s3_intro": "From the project root directory, start all services with:",
        "s3_code1": "docker compose up -d",
        "s3_desc": "This launches MinIO, PostgreSQL, Trino, ClickHouse, and the mc init container.",
        "s3_check": "Check that all services are running:",
        "s3_code2": "docker compose ps",
        "s3_wait": "Wait 20-30 seconds for services to initialize (especially Trino, which takes time to load connectors). Then check logs for any errors:",
        "s3_code3": "docker compose logs --tail=50 trino",
        "s3_note": "Note: If a port is already in use, edit docker-compose.yml and change the left side of the port mapping (e.g., '8081:8080' -> '8082:8080').",
        "s4_title": "Step 1: Fix MinIO Bucket Permissions",
        "s4_intro": "The current docker-compose.yml creates the warehouse bucket with read-only public access. However, the CSV upload tool in query-explorer-ui needs to write files to MinIO. You need to update the mc init container command.",
        "s4_code_title": "In docker-compose.yml, find the mc service and change its command to:",
        "s4_code": "command:\n  - /bin/sh\n  - -c\n  - |\n    sleep 5\n    mc alias set myminio http://minio:9000 minioadmin minioadmin\n    mc mb myminio/warehouse --ignore-existing\n    mc anonymous set public myminio/warehouse\n    mc admin policy set myminio readwrite user=minioadmin",
        "s4_note": "The key thing: the 'warehouse' bucket must allow write access for the CSV upload feature to work. The simplest fix is to use authenticated requests with the MinIO credentials already configured in the frontend service files.",
        "s5_title": "Step 2: Seed ClickHouse with Sample Data",
        "s5_intro": "The data-product-ui dashboard queries three ClickHouse views in the ecommerce_product database:",
        "s5_views": ["ecommerce_product.daily_sales", "ecommerce_product.sales_by_category", "ecommerce_product.top_products"],
        "s5_desc": "These tables/views do not exist yet. You must create them. The easiest way is to create an init SQL file that ClickHouse will run automatically on first startup.",
        "s5_whattodo": "What to do:",
        "s5_step1": "1. Create a folder called clickhouse-init at the project root.",
        "s5_step2": '2. Inside it, create a file called init.sql with the following content:',
        "s5_sql": (
            "CREATE DATABASE IF NOT EXISTS ecommerce_product;\n\n"
            "USE ecommerce_product;\n\n"
            "CREATE TABLE IF NOT EXISTS raw_sales (\n"
            "  sale_date Date,\n"
            "  product_name String,\n"
            "  category String,\n"
            "  quantity UInt32,\n"
            "  unit_price Float64,\n"
            "  total_amount Float64\n"
            ") ENGINE = MergeTree()\n"
            "ORDER BY (sale_date, category);\n\n"
            "INSERT INTO raw_sales VALUES\n"
            "('2025-01-01', 'Wireless Mouse', 'Electronics', 15, 29.99, 449.85),\n"
            "('2025-01-01', 'Desk Lamp', 'Home & Office', 8, 45.00, 360.00),\n"
            "('2025-01-02', 'USB-C Hub', 'Electronics', 22, 34.99, 769.78),\n"
            "('2025-01-02', 'Notebook Set', 'Stationery', 30, 12.50, 375.00),\n"
            "('2025-01-03', 'Mechanical Keyboard', 'Electronics', 10, 89.99, 899.90),\n"
            "('2025-01-03', 'Standing Desk', 'Furniture', 3, 399.00, 1197.00),\n"
            "('2025-01-04', 'Monitor Arm', 'Office', 12, 79.99, 959.88),\n"
            "('2025-01-04', 'Coffee Mug', 'Kitchen', 50, 14.99, 749.50),\n"
            "('2025-01-05', 'Webcam HD', 'Electronics', 18, 59.99, 1079.82),\n"
            "('2025-01-05', 'Desk Organizer', 'Home & Office', 25, 22.99, 574.75);\n\n"
            "CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sales\n"
            "ENGINE = SummingMergeTree()\n"
            "ORDER BY sale_date\n"
            "POPULATE AS\n"
            "SELECT\n"
            "  sale_date,\n"
            "  SUM(quantity) AS units_sold,\n"
            "  SUM(total_amount) AS revenue\n"
            "FROM raw_sales\n"
            "GROUP BY sale_date;\n\n"
            "CREATE MATERIALIZED VIEW IF NOT EXISTS sales_by_category\n"
            "ENGINE = SummingMergeTree()\n"
            "ORDER BY category\n"
            "POPULATE AS\n"
            "SELECT\n"
            "  category,\n"
            "  SUM(quantity) AS units_sold,\n"
            "  SUM(total_amount) AS revenue\n"
            "FROM raw_sales\n"
            "GROUP BY category;\n\n"
            "CREATE MATERIALIZED VIEW IF NOT EXISTS top_products\n"
            "ENGINE = SummingMergeTree()\n"
            "ORDER BY total_revenue DESC\n"
            "POPULATE AS\n"
            "SELECT\n"
            "  product_name,\n"
            "  SUM(quantity) AS units_sold,\n"
            "  SUM(total_amount) AS total_revenue\n"
            "FROM raw_sales\n"
            "GROUP BY product_name\n"
            "ORDER BY total_revenue DESC;"
        ),
        "s5_step3": "3. Add a volume mount for this folder in the clickhouse service in docker-compose.yml:",
        "s5_volcode": (
            "services:\n"
            "  clickhouse:\n"
            "    ...\n"
            "    volumes:\n"
            "      - clickhouse_data:/var/lib/clickhouse\n"
            "      - ./clickhouse-init:/docker-entrypoint-initdb.d   # ADD THIS LINE"
        ),
        "s5_step4": "4. Restart ClickHouse to run the init script:",
        "s5_restart": "docker compose down clickhouse\ndocker compose up -d clickhouse",
        "s5_note": "ClickHouse auto-executes .sql files in /docker-entrypoint-initdb.d/ on first startup. If the clickhouse_data volume already exists, delete it first or use 'docker compose down -v' to force re-initialization.",
        "s6_title": "Step 3: Seed Iceberg Tables via Trino",
        "s6_intro": "The Iceberg catalog is empty -- no tables exist in the s3://warehouse/ location. You can create sample Iceberg tables by connecting to Trino and running DDL statements.",
        "s6_connect_title": "Connect to Trino",
        "s6_connect": "Use the Trino CLI (inside Docker) or any JDBC client:",
        "s6_connect_code": (
            "# Option 1: Trino CLI in Docker\n"
            "docker exec -it data-lakehouse-trino-1 trino\n"
            "\n"
            "# Option 2: Use the web UI at http://localhost:8080/ui"
        ),
        "s6_create_title": "Create Sample Iceberg Tables",
        "s6_create": "Once connected to Trino, run these SQL statements:",
        "s6_sql": (
            "CREATE SCHEMA IF NOT EXISTS iceberg.lakehouse\n"
            "WITH (location = 's3://warehouse/lakehouse');\n"
            "\n"
            "CREATE TABLE IF NOT EXISTS iceberg.lakehouse.products (\n"
            "  product_id BIGINT,\n"
            "  name VARCHAR,\n"
            "  category VARCHAR,\n"
            "  price DOUBLE,\n"
            "  created_at TIMESTAMP\n"
            ") WITH (\n"
            "  format = 'PARQUET',\n"
            "  location = 's3://warehouse/lakehouse/products'\n"
            ");\n"
            "\n"
            "INSERT INTO iceberg.lakehouse.products VALUES\n"
            "  (1, 'Wireless Mouse', 'Electronics', 29.99, TIMESTAMP '2025-01-01 00:00:00'),\n"
            "  (2, 'Desk Lamp', 'Home & Office', 45.00, TIMESTAMP '2025-01-01 00:00:00'),\n"
            "  (3, 'USB-C Hub', 'Electronics', 34.99, TIMESTAMP '2025-01-02 00:00:00'),\n"
            "  (4, 'Mechanical Keyboard', 'Electronics', 89.99, TIMESTAMP '2025-01-03 00:00:00'),\n"
            "  (5, 'Standing Desk', 'Furniture', 399.00, TIMESTAMP '2025-01-03 00:00:00');\n"
            "\n"
            "SELECT * FROM iceberg.lakehouse.products;"
        ),
        "s6_outro": "After seeding, you can explore these tables via the query-explorer-ui at http://localhost:5173.",
        "s7_title": "Step 4: Run the Frontend UIs",
        "s7_intro": "Each UI is a separate Vite dev server. Run them in two terminals.",
        "s7_dashboard_title": "Data Product UI (Dashboard)",
        "s7_dashboard_code": "cd data-product-ui\nnpm run dev",
        "s7_dashboard_desc": "Opens at http://localhost:5174",
        "s7_dashboard_note": "This dashboard shows sales metrics from ClickHouse. ClickHouse must be running and seeded with data for this to work.",
        "s7_explorer_title": "Query Explorer UI",
        "s7_explorer_code": "cd query-explorer-ui\nnpm run dev",
        "s7_explorer_desc": "Opens at http://localhost:5173",
        "s7_explorer_note": "This has two tabs: a SQL query editor (connects to Trino at port 8080) and a CSV upload tool (uploads to MinIO and ingests into ClickHouse).",
        "s7_build_title": "Production Builds",
        "s7_build_desc": "Both apps already have production builds in their dist/ folders. You can serve them with any static file server (e.g., nginx, serve).",
        "s7_build_code": "# Option: serve production build\nnpx serve data-product-ui/dist -l 4173\nnpx serve query-explorer-ui/dist -l 4174",
        "s8_title": "Port Reference",
        "s8_intro": "Here is a quick reference for all the ports used by the project:",
        "s8_ports": [
            ("5173", "Query Explorer UI (dev server)"),
            ("5174", "Data Product UI (dev server)"),
            ("8080", "Trino (REST API & web UI at /ui)"),
            ("5432", "PostgreSQL (Iceberg catalog)"),
            ("9000", "MinIO S3 API"),
            ("9001", "MinIO Console (web UI)"),
            ("8123", "ClickHouse HTTP interface"),
        ],
        "s9_title": "Architecture Diagram",
        "s9_intro": "Below is a textual representation of the system architecture:",
        "s9_diagram": [
            "                          +------------------+",
            "                          |   User Browser   |",
            "                          |  localhost:5173   |",
            "                          |  localhost:5174   |",
            "                          +--------+---------+",
            "                                   |",
            "                    +--------------+--------------+",
            "                    |              |              |",
            "           Vite Proxy        Vite Proxy       Vite Proxy",
            "          /api/clickhouse    /v1/statement     /minio",
            "                    |              |              |",
            "                    v              v              v",
            "              +----------+   +----------+   +----------+",
            "              |ClickHouse|   |  Trino   |   |  MinIO   |",
            "              | :8123    |   | :8080    |   | :9000    |",
            "              +----+-----+   +----+-----+   +----+-----+",
            "                   |              |              |",
            "                   |              |       +------+------+",
            "                   |              |       |   MinIO    |",
            "                   |              |       |  Console   |",
            "                   |              |       |  :9001     |",
            "                   |              |       +------------+",
            "                   |              |",
            "                   |       +------+------+",
            "                   |       | PostgreSQL  |",
            "                   |       | :5432       |",
            "                   |       | (Iceberg    |",
            "                   |       |  Catalog)   |",
            "                   |       +------------+",
        ],
        "s10_title": "Troubleshooting",
        "s10_problems": [
            ("ClickHouse views return no data",
             "The ecommerce_product database and its views need to be created. Follow Step 2 to create the init SQL script and mount it into the ClickHouse container."),
            ("MinIO upload fails (403)",
             "The warehouse bucket has read-only public access. Update the mc init command in docker-compose.yml to grant write access. See Step 1."),
            ("Trino shows no Iceberg tables",
             "The PostgreSQL catalog database might not be initialized. Check that postgres is running and Trino can connect: docker compose logs trino | grep iceberg."),
            ("Port already in use",
             "If a port is already taken, change the left side of the port mapping in docker-compose.yml (e.g., '8081:8080' -> '8082:8080')."),
            ("npm run dev fails",
             "Make sure Node.js v18+ is installed. Delete node_modules and reinstall:\n  cd data-product-ui && rm -rf node_modules && npm install\n  cd query-explorer-ui && rm -rf node_modules && npm install"),
            ("Docker container keeps restarting",
             "Check logs with 'docker compose logs <service-name>'. Common causes: missing dependencies, wrong credentials, or port conflicts."),
            ("Can't connect to Trino from query-explorer-ui",
             "Make sure the Vite proxy in query-explorer-ui/vite.config.js points to the correct Trino URL. Default is http://localhost:8080."),
        ],
        "s11_title": "Next Steps & Ideas",
        "s11_intro": "Once the basic setup is working, here are some ideas for extending the project:",
        "s11_ideas": [
            "Add more sample data - Create larger datasets for both ClickHouse and Iceberg to make the dashboards more interesting.",
            "Set up dbt - Use dbt with the Trino adapter to manage data transformations and materialized views in a more production-like workflow.",
            "Add Superset or Grafana - Connect Apache Superset or Grafana to Trino or ClickHouse for richer visualizations beyond the built-in UIs.",
            "Automate with orchestration - Use Apache Airflow or Dagster to schedule data ingestion and transformation pipelines.",
            "Add a third UI - Build a simple Streamlit or Dash app that queries both Iceberg (via Trino) and ClickHouse for comparison.",
            "Containerize the UIs - Create Dockerfiles for the two React apps and add them to docker-compose.yml so everything runs with one command.",
            "Add CI/CD - Set up GitHub Actions to lint, test, and build the UIs on every push.",
            "Explore Iceberg features - Try time travel queries, schema evolution, and partition evolution using Trino's Iceberg connector.",
        ],
        "final_line1": "Good luck! If you get stuck, check the docker compose logs for each service.",
        "final_line2": "The project root is: E:\\New folder (25)\\data-lakehouse",
    },
    "fr": {
        "header": "Projet Data Lakehouse - Guide d'installation",
        "title": "Data Lakehouse",
        "subtitle": "Guide d'installation et de finalisation du projet",
        "tagline": "Trino + Iceberg + ClickHouse + MinIO",
        "intro1": "Ce guide vous accompagne dans toutes les etapes necessaires pour faire fonctionner la pile complete.",
        "intro2": "Les deux interfaces utilisateur sont deja construites. L'accent est mis sur l'infrastructure et l'initialisation des donnees.",
        "toc_title": "Table des matieres",
        "toc": [
            ("1", "Vue d'ensemble du projet"),
            ("2", "Prerequis"),
            ("3", "Demarrage rapide - Docker Compose"),
            ("4", "Etape 1 : Corriger les permissions du bucket MinIO"),
            ("5", "Etape 2 : Initialiser ClickHouse avec des donnees exemple"),
            ("6", "Etape 3 : Initialiser les tables Iceberg via Trino"),
            ("7", "Etape 4 : Lancer les interfaces utilisateur"),
            ("8", "Reference des ports"),
            ("9", "Diagramme d'architecture"),
            ("10", "Depannage"),
            ("11", "Prochaines etapes et idees"),
        ],
        "s1_title": "Vue d'ensemble du projet",
        "s1_intro": "Il s'agit d'une plateforme data lakehouse moderne qui combine un lac de donnees (MinIO / S3) avec Apache Iceberg (pour les transactions ACID sur le lac), Trino (pour les requetes SQL federees sur plusieurs sources) et ClickHouse (pour l'analytique columnaire rapide).",
        "s1_apps": "Le projet comporte deux applications frontales :",
        "s1_app1": "data-product-ui -- Un tableau de bord d'analytique commerciale affichant le chiffre d'affaires, les unites vendues, les ventes par jour, les ventes par categorie et les produits les plus performants. Interroge les vues ClickHouse dans la base ecommerce_product.",
        "s1_app2": "query-explorer-ui -- Un explorateur de requetes SQL federe avec un navigateur de catalogues/schemas/tables et un outil d'import CSV qui ingere les donnees dans ClickHouse via S3.",
        "s1_note": "Les deux interfaces sont des applications React + Vite. Le code source, les dependances (node_modules) et les builds de production (dist/) sont tous presents. Aucun codage frontal necessaire.",
        "s1_services_title": "Services",
        "s1_services": [
            "MinIO (ports 9000, 9001) -- Stockage objet compatible S3. Bucket racine : warehouse",
            "PostgreSQL (port 5432) -- Stocke les metadonnees du catalogue Iceberg (base : iceberg_catalog)",
            "Trino (port 8080) -- Moteur de requetes SQL distribue open-source",
            "ClickHouse (port 8123) -- Base de donnees analytique columnaire",
            "mc -- Conteneur d'initialisation qui cree le bucket warehouse sur MinIO au demarrage",
        ],
        "s2_title": "Prerequis",
        "s2_intro": "Assurez-vous d'avoir installe les elements suivants avant de commencer :",
        "s2_items": [
            "Docker Desktop (ou Docker Engine + plugin Docker Compose)",
            "Node.js v18+ et npm (pour executer les interfaces hors de Docker)",
            "Un navigateur web (Chrome / Firefox / Edge)",
            "Au moins 8 Go de RAM allouee a Docker",
            "Git (optionnel, pour le controle de version)",
        ],
        "s2_check": "Pour verifier que Docker est pret, executez :",
        "s2_code": "docker compose version\ndocker info",
        "s3_title": "Demarrage rapide - Docker Compose",
        "s3_intro": "Depuis le repertoire racine du projet, lancez tous les services avec :",
        "s3_code1": "docker compose up -d",
        "s3_desc": "Cela lance MinIO, PostgreSQL, Trino, ClickHouse et le conteneur d'initialisation mc.",
        "s3_check": "Verifiez que tous les services fonctionnent :",
        "s3_code2": "docker compose ps",
        "s3_wait": "Attendez 20 a 30 secondes que les services s'initialisent (surtout Trino, qui prend du temps pour charger les connecteurs). Ensuite, verifiez les logs pour d'eventuelles erreurs :",
        "s3_code3": "docker compose logs --tail=50 trino",
        "s3_note": "Remarque : Si un port est deja utilise, modifiez docker-compose.yml et changez le cote gauche du mapping de port (ex : '8081:8080' -> '8082:8080').",
        "s4_title": "Etape 1 : Corriger les permissions du bucket MinIO",
        "s4_intro": "Le fichier docker-compose.yml actuel cree le bucket warehouse avec un acces public en lecture seule. Cependant, l'outil d'import CSV dans query-explorer-ui doit ecrire des fichiers dans MinIO. Vous devez mettre a jour la commande du conteneur d'initialisation mc.",
        "s4_code_title": "Dans docker-compose.yml, trouvez le service mc et modifiez sa commande :",
        "s4_code": "command:\n  - /bin/sh\n  - -c\n  - |\n    sleep 5\n    mc alias set myminio http://minio:9000 minioadmin minioadmin\n    mc mb myminio/warehouse --ignore-existing\n    mc anonymous set public myminio/warehouse\n    mc admin policy set myminio readwrite user=minioadmin",
        "s4_note": "Le point essentiel : le bucket 'warehouse' doit autoriser l'ecriture pour que l'import CSV fonctionne. La solution la plus simple est d'utiliser des requetes authentifiees avec les identifiants MinIO deja configures dans les fichiers de service frontaux.",
        "s5_title": "Etape 2 : Initialiser ClickHouse avec des donnees exemple",
        "s5_intro": "Le tableau de bord data-product-ui interroge trois vues ClickHouse dans la base de donnees ecommerce_product :",
        "s5_views": ["ecommerce_product.daily_sales", "ecommerce_product.sales_by_category", "ecommerce_product.top_products"],
        "s5_desc": "Ces tables/vues n'existent pas encore. Vous devez les creer. Le moyen le plus simple est de creer un fichier SQL d'initialisation que ClickHouse executera automatiquement au premier demarrage.",
        "s5_whattodo": "Marche a suivre :",
        "s5_step1": "1. Creez un dossier appele clickhouse-init a la racine du projet.",
        "s5_step2": "2. A l'interieur, creez un fichier nomme init.sql avec le contenu suivant :",
        "s5_sql": (
            "CREATE DATABASE IF NOT EXISTS ecommerce_product;\n\n"
            "USE ecommerce_product;\n\n"
            "CREATE TABLE IF NOT EXISTS raw_sales (\n"
            "  sale_date Date,\n"
            "  product_name String,\n"
            "  category String,\n"
            "  quantity UInt32,\n"
            "  unit_price Float64,\n"
            "  total_amount Float64\n"
            ") ENGINE = MergeTree()\n"
            "ORDER BY (sale_date, category);\n\n"
            "INSERT INTO raw_sales VALUES\n"
            "('2025-01-01', 'Wireless Mouse', 'Electronics', 15, 29.99, 449.85),\n"
            "('2025-01-01', 'Desk Lamp', 'Home & Office', 8, 45.00, 360.00),\n"
            "('2025-01-02', 'USB-C Hub', 'Electronics', 22, 34.99, 769.78),\n"
            "('2025-01-02', 'Notebook Set', 'Stationery', 30, 12.50, 375.00),\n"
            "('2025-01-03', 'Mechanical Keyboard', 'Electronics', 10, 89.99, 899.90),\n"
            "('2025-01-03', 'Standing Desk', 'Furniture', 3, 399.00, 1197.00),\n"
            "('2025-01-04', 'Monitor Arm', 'Office', 12, 79.99, 959.88),\n"
            "('2025-01-04', 'Coffee Mug', 'Kitchen', 50, 14.99, 749.50),\n"
            "('2025-01-05', 'Webcam HD', 'Electronics', 18, 59.99, 1079.82),\n"
            "('2025-01-05', 'Desk Organizer', 'Home & Office', 25, 22.99, 574.75);\n\n"
            "CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sales\n"
            "ENGINE = SummingMergeTree()\n"
            "ORDER BY sale_date\n"
            "POPULATE AS\n"
            "SELECT\n"
            "  sale_date,\n"
            "  SUM(quantity) AS units_sold,\n"
            "  SUM(total_amount) AS revenue\n"
            "FROM raw_sales\n"
            "GROUP BY sale_date;\n\n"
            "CREATE MATERIALIZED VIEW IF NOT EXISTS sales_by_category\n"
            "ENGINE = SummingMergeTree()\n"
            "ORDER BY category\n"
            "POPULATE AS\n"
            "SELECT\n"
            "  category,\n"
            "  SUM(quantity) AS units_sold,\n"
            "  SUM(total_amount) AS revenue\n"
            "FROM raw_sales\n"
            "GROUP BY category;\n\n"
            "CREATE MATERIALIZED VIEW IF NOT EXISTS top_products\n"
            "ENGINE = SummingMergeTree()\n"
            "ORDER BY total_revenue DESC\n"
            "POPULATE AS\n"
            "SELECT\n"
            "  product_name,\n"
            "  SUM(quantity) AS units_sold,\n"
            "  SUM(total_amount) AS total_revenue\n"
            "FROM raw_sales\n"
            "GROUP BY product_name\n"
            "ORDER BY total_revenue DESC;"
        ),
        "s5_step3": "3. Ajoutez un montage de volume pour ce dossier dans le service clickhouse dans docker-compose.yml :",
        "s5_volcode": (
            "services:\n"
            "  clickhouse:\n"
            "    ...\n"
            "    volumes:\n"
            "      - clickhouse_data:/var/lib/clickhouse\n"
            "      - ./clickhouse-init:/docker-entrypoint-initdb.d   # AJOUTEZ CETTE LIGNE"
        ),
        "s5_step4": "4. Redemarrez ClickHouse pour executer le script d'initialisation :",
        "s5_restart": "docker compose down clickhouse\ndocker compose up -d clickhouse",
        "s5_note": "ClickHouse execute automatiquement les fichiers .sql dans /docker-entrypoint-initdb.d/ au premier demarrage. Si le volume clickhouse_data existe deja, supprimez-le d'abord ou utilisez 'docker compose down -v' pour forcer la reinitalisation.",
        "s6_title": "Etape 3 : Initialiser les tables Iceberg via Trino",
        "s6_intro": "Le catalogue Iceberg est vide -- aucune table n'existe dans l'emplacement s3://warehouse/. Vous pouvez creer des tables Iceberg exemple en vous connectant a Trino et en executant des instructions DDL.",
        "s6_connect_title": "Se connecter a Trino",
        "s6_connect": "Utilisez la CLI Trino (dans Docker) ou un client JDBC :",
        "s6_connect_code": (
            "# Option 1 : CLI Trino dans Docker\n"
            "docker exec -it data-lakehouse-trino-1 trino\n"
            "\n"
            "# Option 2 : Utilisez l'interface web sur http://localhost:8080/ui"
        ),
        "s6_create_title": "Creer des tables Iceberg exemple",
        "s6_create": "Une fois connecte a Trino, executez ces instructions SQL :",
        "s6_sql": (
            "CREATE SCHEMA IF NOT EXISTS iceberg.lakehouse\n"
            "WITH (location = 's3://warehouse/lakehouse');\n"
            "\n"
            "CREATE TABLE IF NOT EXISTS iceberg.lakehouse.products (\n"
            "  product_id BIGINT,\n"
            "  name VARCHAR,\n"
            "  category VARCHAR,\n"
            "  price DOUBLE,\n"
            "  created_at TIMESTAMP\n"
            ") WITH (\n"
            "  format = 'PARQUET',\n"
            "  location = 's3://warehouse/lakehouse/products'\n"
            ");\n"
            "\n"
            "INSERT INTO iceberg.lakehouse.products VALUES\n"
            "  (1, 'Wireless Mouse', 'Electronics', 29.99, TIMESTAMP '2025-01-01 00:00:00'),\n"
            "  (2, 'Desk Lamp', 'Home & Office', 45.00, TIMESTAMP '2025-01-01 00:00:00'),\n"
            "  (3, 'USB-C Hub', 'Electronics', 34.99, TIMESTAMP '2025-01-02 00:00:00'),\n"
            "  (4, 'Mechanical Keyboard', 'Electronics', 89.99, TIMESTAMP '2025-01-03 00:00:00'),\n"
            "  (5, 'Standing Desk', 'Furniture', 399.00, TIMESTAMP '2025-01-03 00:00:00');\n"
            "\n"
            "SELECT * FROM iceberg.lakehouse.products;"
        ),
        "s6_outro": "Apres l'initialisation, vous pouvez explorer ces tables via query-explorer-ui sur http://localhost:5173.",
        "s7_title": "Etape 4 : Lancer les interfaces utilisateur",
        "s7_intro": "Chaque interface est un serveur de dev Vite separe. Lancez-les dans deux terminaux.",
        "s7_dashboard_title": "Interface Data Product (Tableau de bord)",
        "s7_dashboard_code": "cd data-product-ui\nnpm run dev",
        "s7_dashboard_desc": "S'ouvre sur http://localhost:5174",
        "s7_dashboard_note": "Ce tableau de bord affiche les mesures de ventes depuis ClickHouse. ClickHouse doit etre en cours d'execution et initialise avec des donnees.",
        "s7_explorer_title": "Interface Query Explorer",
        "s7_explorer_code": "cd query-explorer-ui\nnpm run dev",
        "s7_explorer_desc": "S'ouvre sur http://localhost:5173",
        "s7_explorer_note": "Elle comporte deux onglets : un editeur de requetes SQL (connecte a Trino sur le port 8080) et un outil d'import CSV (televerse vers MinIO et importe dans ClickHouse).",
        "s7_build_title": "Builds de production",
        "s7_build_desc": "Les deux applications ont deja des builds de production dans leurs dossiers dist/. Vous pouvez les servir avec n'importe quel serveur de fichiers statique (ex : nginx, serve).",
        "s7_build_code": "# Option : servir le build de production\nnpx serve data-product-ui/dist -l 4173\nnpx serve query-explorer-ui/dist -l 4174",
        "s8_title": "Reference des ports",
        "s8_intro": "Voici une reference rapide de tous les ports utilises par le projet :",
        "s8_ports": [
            ("5173", "Query Explorer UI (serveur de dev)"),
            ("5174", "Data Product UI (serveur de dev)"),
            ("8080", "Trino (API REST et interface web sur /ui)"),
            ("5432", "PostgreSQL (catalogue Iceberg)"),
            ("9000", "API S3 MinIO"),
            ("9001", "Console MinIO (interface web)"),
            ("8123", "Interface HTTP ClickHouse"),
        ],
        "s9_title": "Diagramme d'architecture",
        "s9_intro": "Voici une representation textuelle de l'architecture du systeme :",
        "s9_diagram": [
            "                          +------------------+",
            "                          |   Navigateur    |",
            "                          |  localhost:5173   |",
            "                          |  localhost:5174   |",
            "                          +--------+---------+",
            "                                   |",
            "                    +--------------+--------------+",
            "                    |              |              |",
            "           Vite Proxy        Vite Proxy       Vite Proxy",
            "          /api/clickhouse    /v1/statement     /minio",
            "                    |              |              |",
            "                    v              v              v",
            "              +----------+   +----------+   +----------+",
            "              |ClickHouse|   |  Trino   |   |  MinIO   |",
            "              | :8123    |   | :8080    |   | :9000    |",
            "              +----+-----+   +----+-----+   +----+-----+",
            "                   |              |              |",
            "                   |              |       +------+------+",
            "                   |              |       |  Console  |",
            "                   |              |       |  MinIO    |",
            "                   |              |       |  :9001    |",
            "                   |              |       +------------+",
            "                   |              |",
            "                   |       +------+------+",
            "                   |       | PostgreSQL  |",
            "                   |       | :5432       |",
            "                   |       | (Catalogue  |",
            "                   |       |  Iceberg)   |",
            "                   |       +------------+",
        ],
        "s10_title": "Depannage",
        "s10_problems": [
            ("Les vues ClickHouse ne retournent aucune donnee",
             "La base de donnees ecommerce_product et ses vues doivent etre creees. Suivez l'Etape 2 pour creer le script SQL d'initialisation et le monter dans le conteneur ClickHouse."),
            ("L'import MinIO echoue (403)",
             "Le bucket warehouse a un acces public en lecture seule. Mettez a jour la commande mc dans docker-compose.yml pour autoriser l'ecriture. Voir Etape 1."),
            ("Trino n'affiche aucune table Iceberg",
             "La base de donnees du catalogue PostgreSQL n'est peut-etre pas initialisee. Verifiez que postgres fonctionne et que Trino peut se connecter : docker compose logs trino | grep iceberg."),
            ("Port deja utilise",
             "Si un port est deja pris, modifiez le cote gauche du mapping de port dans docker-compose.yml (ex : '8081:8080' -> '8082:8080')."),
            ("npm run dev echoue",
             "Assurez-vous que Node.js v18+ est installe. Supprimez node_modules et reinstallez :\n  cd data-product-ui && rm -rf node_modules && npm install\n  cd query-explorer-ui && rm -rf node_modules && npm install"),
            ("Le conteneur Docker redemarre sans cesse",
             "Verifiez les logs avec 'docker compose logs <nom-service>'. Causes courantes : dependances manquantes, mauvais identifiants ou conflits de ports."),
            ("Impossible de se connecter a Trino depuis query-explorer-ui",
             "Assurez-vous que le proxy Vite dans query-explorer-ui/vite.config.js pointe vers la bonne URL Trino. La valeur par defaut est http://localhost:8080."),
        ],
        "s11_title": "Prochaines etapes et idees",
        "s11_intro": "Une fois la configuration de base fonctionnelle, voici quelques idees pour prolonger le projet :",
        "s11_ideas": [
            "Ajouter plus de donnees exemple - Creez des jeux de donnees plus volumineux pour ClickHouse et Iceberg afin de rendre les tableaux de bord plus interessants.",
            "Mettre en place dbt - Utilisez dbt avec l'adaptateur Trino pour gerer les transformations de donnees et les vues materialisees dans un flux de travail plus professionnel.",
            "Ajouter Superset ou Grafana - Connectez Apache Superset ou Grafana a Trino ou ClickHouse pour des visualisations plus riches au-dela des interfaces integrees.",
            "Automatiser avec un orchestrateur - Utilisez Apache Airflow ou Dagster pour planifier les pipelines d'ingestion et de transformation de donnees.",
            "Ajouter une troisieme interface - Construisez une application simple Streamlit ou Dash qui interroge a la fois Iceberg (via Trino) et ClickHouse pour comparaison.",
            "Containeriser les interfaces - Creez des Dockerfiles pour les deux applications React et ajoutez-les a docker-compose.yml pour que tout fonctionne avec une seule commande.",
            "Ajouter CI/CD - Mettez en place des GitHub Actions pour lint, tester et builder les interfaces a chaque push.",
            "Explorer les fonctionnalites Iceberg - Essayez les requetes de voyage dans le temps, l'evolution de schema et l'evolution de partition avec le connecteur Iceberg de Trino.",
        ],
        "final_line1": "Bonne chance ! Si vous etes bloque, consultez les logs docker compose pour chaque service.",
        "final_line2": "La racine du projet est : E:\\New folder (25)\\data-lakehouse",
    },
}


def build_pdf(lang, c):
    pdf = PDF()
    pdf.header_title = c["header"]
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title page
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(0, 15, c["title"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 12, c["subtitle"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, c["tagline"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(25)

    pdf.set_draw_color(25, 60, 120)
    pdf.line(60, pdf.get_y(), pdf.w - 60, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, c["intro1"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, c["intro2"], align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.add_page()

    # --- TABLE OF CONTENTS ---
    pdf.chapter_title("", c["toc_title"])
    pdf.set_font("Helvetica", "", 11)
    for num, title in c["toc"]:
        pdf.set_text_color(25, 60, 120)
        pdf.cell(10, 7, num)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")

    # --- SECTION 1 ---
    pdf.add_page()
    pdf.chapter_title("1", c["s1_title"])
    pdf.body_text(c["s1_intro"])
    pdf.body_text(c["s1_apps"])
    pdf.bullet(c["s1_app1"])
    pdf.bullet(c["s1_app2"])
    pdf.body_text(c["s1_note"])
    pdf.ln(2)
    pdf.section_title(c["s1_services_title"])
    for s in c["s1_services"]:
        pdf.bullet(s)

    # --- SECTION 2 ---
    pdf.add_page()
    pdf.chapter_title("2", c["s2_title"])
    pdf.body_text(c["s2_intro"])
    for item in c["s2_items"]:
        pdf.bullet(item)
    pdf.ln(2)
    pdf.body_text(c["s2_check"])
    pdf.code_block(c["s2_code"])

    # --- SECTION 3 ---
    pdf.add_page()
    pdf.chapter_title("3", c["s3_title"])
    pdf.body_text(c["s3_intro"])
    pdf.code_block(c["s3_code1"])
    pdf.body_text(c["s3_desc"])
    pdf.body_text(c["s3_check"])
    pdf.code_block(c["s3_code2"])
    pdf.body_text(c["s3_wait"])
    pdf.code_block(c["s3_code3"])
    pdf.note_box(c["s3_note"])

    # --- SECTION 4 ---
    pdf.add_page()
    pdf.chapter_title("4", c["s4_title"])
    pdf.body_text(c["s4_intro"])
    pdf.body_text(c["s4_code_title"])
    pdf.code_block(c["s4_code"])
    pdf.note_box(c["s4_note"])

    # --- SECTION 5 ---
    pdf.add_page()
    pdf.chapter_title("5", c["s5_title"])
    pdf.body_text(c["s5_intro"])
    for v in c["s5_views"]:
        pdf.bullet(v)
    pdf.body_text(c["s5_desc"])
    pdf.ln(2)
    pdf.section_title(c["s5_whattodo"])
    pdf.body_text(c["s5_step1"])
    pdf.body_text(c["s5_step2"])
    pdf.code_block(c["s5_sql"])
    pdf.body_text(c["s5_step3"])
    pdf.code_block(c["s5_volcode"])
    pdf.body_text(c["s5_step4"])
    pdf.code_block(c["s5_restart"])
    pdf.note_box(c["s5_note"])

    # --- SECTION 6 ---
    pdf.add_page()
    pdf.chapter_title("6", c["s6_title"])
    pdf.body_text(c["s6_intro"])
    pdf.ln(2)
    pdf.section_title(c["s6_connect_title"])
    pdf.body_text(c["s6_connect"])
    pdf.code_block(c["s6_connect_code"])
    pdf.ln(2)
    pdf.section_title(c["s6_create_title"])
    pdf.body_text(c["s6_create"])
    pdf.code_block(c["s6_sql"])
    pdf.body_text(c["s6_outro"])

    # --- SECTION 7 ---
    pdf.add_page()
    pdf.chapter_title("7", c["s7_title"])
    pdf.body_text(c["s7_intro"])
    pdf.ln(2)
    pdf.section_title(c["s7_dashboard_title"])
    pdf.code_block(c["s7_dashboard_code"])
    pdf.body_text(c["s7_dashboard_desc"])
    pdf.body_text(c["s7_dashboard_note"])
    pdf.ln(4)
    pdf.section_title(c["s7_explorer_title"])
    pdf.code_block(c["s7_explorer_code"])
    pdf.body_text(c["s7_explorer_desc"])
    pdf.body_text(c["s7_explorer_note"])
    pdf.ln(4)
    pdf.section_title(c["s7_build_title"])
    pdf.body_text(c["s7_build_desc"])
    pdf.code_block(c["s7_build_code"])

    # --- SECTION 8 ---
    pdf.add_page()
    pdf.chapter_title("8", c["s8_title"])
    pdf.body_text(c["s8_intro"])
    pdf.set_font("Helvetica", "", 10)
    pdf.set_fill_color(245, 245, 250)
    pdf.set_draw_color(200, 200, 210)
    for i, (port, desc) in enumerate(c["s8_ports"]):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 250)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(30, 8, port, border=1, fill=True, align="C")
        pdf.cell(0, 8, desc, border=1, fill=True)
        pdf.ln()

    # --- SECTION 9 ---
    pdf.add_page()
    pdf.chapter_title("9", c["s9_title"])
    pdf.body_text(c["s9_intro"])
    pdf.ln(2)
    pdf.set_font("Courier", "", 8.5)
    for line in c["s9_diagram"]:
        pdf.cell(0, 4.2, line, new_x="LMARGIN", new_y="NEXT")

    # --- SECTION 10 ---
    pdf.add_page()
    pdf.chapter_title("10", c["s10_title"])
    pdf.ln(2)
    for problem, solution in c["s10_problems"]:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(180, 50, 50)
        pdf.cell(0, 7, problem, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5.5, "  " + solution)
        pdf.ln(3)

    # --- SECTION 11 ---
    pdf.add_page()
    pdf.chapter_title("11", c["s11_title"])
    pdf.body_text(c["s11_intro"])
    pdf.ln(2)
    for i, idea in enumerate(c["s11_ideas"], 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(25, 60, 120)
        pdf.cell(8, 7, f"{i}.")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5.5, idea)
        pdf.ln(2)

    # --- FINAL NOTE ---
    pdf.ln(6)
    pdf.set_draw_color(25, 60, 120)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, c["final_line1"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, c["final_line2"], align="C", new_x="LMARGIN", new_y="NEXT")

    suffix = "EN" if lang == "en" else "FR"
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"Data_Lakehouse_Setup_Guide_{suffix}.pdf",
    )
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


for lang in ("en", "fr"):
    build_pdf(lang, CONTENT[lang])
