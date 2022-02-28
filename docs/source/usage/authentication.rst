**************
Authentication
**************

In order to use the EnSysMod application, you must first create an account. There are no special permissions or
restrictions for now. Its just a simple account to prevent data manipulation on datasets created by other users.

Register
========
You can create an account by executing the following REST API call:

.. openapi:: ./../generated/openapi.json
   :paths:
      /auth/register

You need a **username** and a **password**.

Login
=====
After creating an account, you can log in by executing the following REST API call:

.. openapi:: ./../generated/openapi.json
   :paths:
      /auth/login

As response you get an access token. All further requests must be authenticated with this token.

Authenticate for using API docs
===============================
Use the authentication button on the top right corner of the documentation page.

