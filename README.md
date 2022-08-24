# ThousandEyes API Framework

This is a framework that connects to the API of ThousandEyes software.

## Authentication

Credentials are obtained by navigating the ThousandEyes website and granting API permissions. As of the most recent update, HTTP Basic is configured.

Credentials for HTTP Basic Authentication are passed as parameters when instantiating the `thousand_eyes` object.

## Getting Started

To instantiate a `thousand_eyes` object, pass a string of the credential name created in the "Authentication" section :

```
>>> api_username = ''
>>> api_password = ''
>>> t = thousand_eyes(api_username, api_password)
```

Then, if an AID is required to access a business unit :

The AID is hard-coded in the `initialize_aid()` function :
```
    ...
	if account['accountGroupName'] == 'Your Company':
    ...
```

Then call the function to add the AID into the authentication parameters :
```
>>> te.initialize_aid()
```

## ThousandEyes Features

Most features of the API to retrieve data are written :
- Basic Status check
- List account groups
- List tests
- List agents
- List agents by type
- List alert rules
- List alerts
- List alert integrations
- List alert suppression windows
- List labels
- List BGP monitors
- List reports
- List report data
- List report snapshots
- List report snapshot data
- List users
- List roles
- List permissions
- List usage
- List endpoint user sessions
- List endpoint web pages
- List endpoint network sessions
- List endpoint network topologies
- List endpoint agents
- List endpoint networks
- Get single test by name
- Get single test by server

A few custom scripts were added to modify data :
- Creating tests    (custom)
- Deleting tests
- Enabling alerts
- Disabling alerts
- Updating fields on alerts

The custom scripts were created to a specific criteria, matching device names according to my own standards.
- `test_create()`
- `test_standardize()`
These would need to be modified to fit your own standards.