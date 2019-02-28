# :skull: backEnd (SWE Society Website)
### developing on django (2.0 or up)
***
### database : postgresql (10.0)
 * #### Name: *****
 * #### Password: *****
 * #### Database: *****
 * #### Host: ******
 * #### Port: *****

#### Server: *******
### For Production  
`import dj_database_url
 DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
 `
***

## Workflow:

### urls:
  * #### example.com/ (template = index.html)
  * #### example.com/login (template = login.html) [not dialog view]```no registration page```
  * #### example.com/opensource (template = opensource.html) [view is not comfirmed yet, will be updated]
  * #### example.com/id (template = profile.html) [see profile structure](https://github.com/swesust/front-end)
  * #### example.com/batch (template = batchlist.html) [all batch list]
  * #### example.com/batch/2017 (template = batch.html)[every particular batch students]
  * #### example.com/faculty (template = faculty.html) [teachers list]
  
### templates:
#### `base.html` will carry the base header and a content block. Every extended or inherited .html file will set on the content block of the base view

#### `prototype of base.html`
```html
<!DOCTYPE html>
<html>
<head>

	<link rel="stylesheet" type="text/css" href="">
	<script type="text/javascript"></script>

	{% block extra_head %}

	<!-- extended page header -->

	{% endblock %}

</head>
<body>
 	
 	<div class="header"></div>

 	{% block contents %}

 	<!-- extended page contents -->

 	{% endblock %}

 	<div class="footer"></div>

</body>
</html>

```

#### `prototype of other templates`
```html
{% extends 'base.html' %}
{% load staticfiles %}

{% extra_head %}
	
	<title></title>
	<link rel="stylesheet" type="text/css" href="">
	<script type="text/javascript"></script>

{% endblock %}


{% block contents %}

<div class="contents">
	
	<!-- page contents -->

</div>

{% endblock %}

```

***
### User profile and authentication:
![](doc/auth_model.png)

#### `User types`


General | Staff | Super
--- | --- | --- 
Can only log in into site have no permission to visit admin panel | Can log in into site and have the permission to visit admin panel and also have some limited permission on admin panel functionality | Can log in into site and admin panel and have every permission. Super user will destroy after deploying. Available in developing version.
