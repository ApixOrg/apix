
[<img src="https://www.apix.org/apix-logo-dark-mode.png" height="200">](https://apix.org)



---

**Documentation**: https://apix.org

**Source Code**: https://github.com/ApixOrg/apix

---

**apiX** is a full-stack framework for backend developlment. **apiX** integrates all necessary components to create 
powerful backend applications in Python with just a few lines of code. Use **apiX** to create with ease 
-backed applications with a [GraphQL]() API . 

## Integrated technologies

- [MongoDB](https://www.mongodb.com): The schemaless and document-oriented database is ideal to effortlessly create powerful applications from scratch.
- [GraphQL](https://graphql.org): The query language for APIs is perfectly suited to create efficient and well-documented APIs.
- [Google Cloud Storage](https://cloud.google.com/storage): The powerful object storage from Google allows you store data of any size and format.

## Installation

The **apiX** library is published on [PyPI](https://pypi.org/project/apix-core/) and can be installed with the following pip command.

```commandline
pip install apix-core
```

You can use [Uvicorn](https://www.uvicorn.org) to run the application. Uvicorn is an ASGI web server implementation for Python. To install apiX together with uvicorn run this pip command.

```commandline
pip install 'apix-core[uvicorn]'
```

## Documentation

Go to our website [apix.org](https://apix.org) and check out the detailed documentation.

## Example App

Make sure that you have **apiX** and **uvicorn** installed. Before you run the python code, replace the CONNECTION_STRING placeholder
with the connection string to your MongoDB instance.

```python 
import uvicorn
from apix.app import ApixApp
from apix.attribute import ApixIntegerAttribute, ApixStringAttribute
from apix.database import ApixDatabase
from apix.model import ApixModel
from apix.resolver import ApixMutationResolver, ApixQueryResolver
from apix.scalar import ApixString


# Connection details of your MongoDB instance
Database = ApixDatabase(
    host='CONNECTION_STRING',
    name='demo',
)


# User model definition
User = ApixModel(
    name='user',
    attributes=[
        ApixStringAttribute('name'),
        ApixIntegerAttribute('age'),
    ],
)


# Function to create a user
def create_user(user: User) -> User:
    Database(User).insert_one(user)
    return user


# Function to find a user by name
def find_user_by_name(name: ApixString) -> User:
    return Database(User).find_one(User.Name.Equal(name))


# Create the app
app = ApixApp(
    resolvers=[
        ApixMutationResolver(create_user),
        ApixQueryResolver(find_user_by_name),
    ],
)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='localhost',
        port=8080,
    )

```

Once your app is running, the GraphQL API is available at [http://localhost:8080/graphql](). Now open your favorite web client (such as [Insomnia](https://insomnia.rest) or [Postman](https://www.postman.com)) 
and create a user with the following request.

```graphql
mutation {
    createUser(
        user: {
            name: "Dan"
            age: 30
        }
    ) {
        id
        name
        age
    }
}
```

To search for the user by name you can use the request below.

```graphql
query {
    findUserByName(
        name: "Dan"
    ) {
        id
        name
        age
    }
}
```


