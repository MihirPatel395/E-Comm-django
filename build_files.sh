echo "BUILD Start"
# build_files.sh
pip install -r requirements.txt

# echo "Migrating Databases"
# python3 manage.py makemigrations --noinput
# python3 manage.py migrate --noinput

echo "Collecting Static Files"
python3.9 manage.py collectstatic --noinput

echo "BUILD End"
