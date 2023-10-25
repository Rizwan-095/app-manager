# About Application
This is a back-end application in django rest framework. The users can create, retrieve, update and delete the applications. Users can create account, login and reset the password via email verification link. Users can upgrade the subscriptions plans of the apps.
# Usage
1. Create an account
2. Activate and verify the account via email. **You will not be able to login without email verification**
3. Login to account
4. Create, update, retrieve all, retrieve single and delete apps
5. Upgrade subscriptions plans
# Setup
* rename example.env to .env
* enter the variable values inside .env file
``` sh
python3 -m virtualenv myenv
```
```
source myenv/bin/activate
```
```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
```
python manage.py runserver
```
# APIs
Please see thunder-collection_app_manager.json file for example usage.
## account
1. **POST** https://app-manager-five.vercel.app/account/register/
```json
{
"first_name": "Ahsan",
"last_name": "Umair",
"email": "ahsan@gmail.com",
"password": "Secret123@",
"confirm_password": "Secret123@"
}
```
2. **POST** https://app-manager-five.vercel.app/account/login/
 ```json
{
"email": "ahsan@gmail.com",
"password": "Secret123@"
}
```
3. **POST** https://app-manager-five.vercel.app/account/forgot-password/
```json
{
"email": "ahsan@gmail.com"
}
```
## app_manager
1. **POST** https://app-manager-five.vercel.app/app/create-app/
```json
{
"name": "facebook",
"description": "This is my facebook."
}
```
2. **GET** https://app-manager-five.vercel.app/app/get-all-apps/
3. **GET** https://app-manager-five.vercel.app/app/get-single-app/1/ (1 is app_id)
4. **PUT** https://app-manager-five.vercel.app/app/update-app/1/ (1 is app_id)
``` json
{
"name": "my-app3",
"description": "This is my app3."
}
```
5. **DELETE** https://app-manager-five.vercel.app/app/delete-app/1/ (1 is app_id)
6. **POST** https://app-manager-five.vercel.app/app/upgrade-plan/1/ (1 is app_id)
``` json
{
"plan": "standard",
"price": 10
}
```
# Run Docker
```
docker-compose build
```
```
docker-compose up -d
```
