# Portfolio Manager

This project has the goal of providing an API to access the projects in my portfolio, as well as having an administration panel where I can add, edit or delete them.

## Endpoints

### **Projects list**

Returns a list of all projects
- **method:** `GET`
- **url:** `/api/projects/`
- **Query parameters**:
    - `preview`: Shows minimal information about each project
- **success response**: 
   - Code: `200 OK`
   - Content example (with `preview` option passed:

```
[
    {
        "id": 3,
        "name": "Foo Project",
        "role": "Full-stack developer",
        "cover_image": "http://localhost:8000/media/screenshots/Foo%20Project/Screenshot_from_2021-02-24_18-50-22.png"
    }
]
```


### Project details

Returns all the information about a particular project: Its `id`, `name`, my `role` in the project, the project's `description`, its `year`, the `technologies` used, and the project's `screenshots`

- **method:** `GET`
- **url:** `/api/projects/:pk/`
- **success response**: 
   - Code: `200 OK`
   - Content example:

```
{
    "id": 3,
    "name": "Foo Project",
    "role": "Full-stack developer",
    "description": "Lorem ipsum dolor sit amet.",
    "year": 2017,
    "technologies": [
        {
            "id": 3,
            "how": "Django allowed me to ...",
            "technology_name": "Django",
            "technology_logo": "http://localhost:8000/media/technologies_logos/django.jpeg"
        },
        {
            "id": 4,
            "how": "In this project, JS allowed me to...",
            "technology_name": "JS",
            "technology_logo": "http://localhost:8000/media/technologies_logos/idea.jpeg"
        }
    ],
    "screenshots": [
        {
            "id": 2,
            "image": "http://localhost:8000/media/screenshots/Foo%20Project/Screenshot_from_2021-02-24_18-50-22.png",
            "is_cover": true,
            "caption": "Main screenshot",
            "project": 3
        },
        {
            "id": 3,
            "image": "http://localhost:8000/media/screenshots/Foo%20Project/idea.jpeg",
            "is_cover": false,
            "caption": "Another screenshot",
            "project": 3
        }
    ]
}
```
