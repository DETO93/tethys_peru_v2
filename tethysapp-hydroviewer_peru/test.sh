cd /var/www/html
sudo chown -R $USER static/
sudo chown -R $USER workspaces/
tethys manage collectall
sudo chown -R www-data  static/
sudo chown -R www-data  workspaces/
sudo systemctl restart nginx
sudo systemctl restart supervisor