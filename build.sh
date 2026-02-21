cat <<EOF > build.sh
#!/bin/bash
echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
# --clear bayrağı eski kalıntıları temizler
python3.12 manage.py collectstatic --noinput --clear

echo "Running migrations..."
python3.12 manage.py migrate
EOF