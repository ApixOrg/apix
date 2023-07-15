
[<img src="https://drive.google.com/uc?id=15TdAvzjAKX-IiyyzzAdgb76KWAR8EKRz" height="200">](https://apix.org)



---

**Documentation**: https://apix.org (in progress)

**Source Code**: https://github.com/ApixOrg/apix

---

**apiX** is a framework to create MongoDB-backed applications with a GraphQL API web interface. 
**apiX** drastically simplifies the linkage between the backend and the web interface. 
**apiX** enables you to build applications in a beautiful pythonic way without dealing with
technical libraries, such as, [pymongo](https://pymongo.readthedocs.io/en/stable/) for MongoDB operations 
and [graphql-core](https://graphql-core-3.readthedocs.io/en/latest/) for the GraphQL API. 

## Installation

**apiX** is available on PyPI and can be installed with pip.

```commandline
pip install apix
```

You can also directly install the latest version from Github.

```commandline
pip install git+https:://github.com/ApixOrg/apix.git
```

## Why use MongoDB and GraphQL?

|                 | [<img src="https://drive.google.com/uc?id=1r3hrQhF0Ry8mH_7QzYr4VQaOUJhnXku5" height="50">](https://mongodb.com)                                    | [<img src="https://drive.google.com/uc?id=1E572-jLp5LAQXAqk-74tE3pi7xYEtc3j" height="50">](https://graphql.org)                                            |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Description** | MongoDB is a schemaless database that stores arbitrary JSON objects (so called "Documents").                                                       | GraphQL is a flexible query language for APIs that allows you to specify exactly the fields which you want to request.                                     |
| **Advantages**  | 1. Create document collections on-the-fly. <br/> 2. Documents can be nested and contain arrays. <br/> 3. Powerful data platform in the cloud available. | 1. Reduce the amount of data transmitted. <br/> 2. The requests are strictly type-safe. <br/>  3. Multiple resources can be collected in a single request. |
| **Article**     | [Why use MongoDB?](https://www.mongodb.com/why-use-mongodb)                                                                                        | [Why use GraphQL?](https://www.apollographql.com/blog/graphql/basics/why-use-graphql)                                                                      |

## Example App

Make sure that you have **apiX** and **uvicorn** installed. Before you run the python code, replace the CONNECTION_STRING placeholder
with the connection string to your MongoDB instance.

```python 
import uvicorn
from apix import *


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
def find_user_by_name(name: str) -> User:
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

Once your app is running, the GraphQL API web interface is available at [http://localhost:8080/graphql](). Now open your favorite web client (such as [Insomnia](https://insomnia.rest) or [Postman](https://www.postman.com)) 
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


