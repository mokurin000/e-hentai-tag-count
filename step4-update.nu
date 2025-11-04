aria2c -x 16 -s 32 -c https://github.com/URenko/e-hentai-db/releases/download/nightly/nightly.sql.zstd
zstd -d nightly.sql.zstd
$env.PATH = ($env.PATH | append 'C:\Program Files\MariaDB 11.7\bin\')
open -r perf.sql | mariadb -u root --password=123456 e-hentai-db

uv run step2-export_data.py --first-run
uv run step3-manual_fix.py
uv run step2-export_data.py

rm -f nightly.sql.*
