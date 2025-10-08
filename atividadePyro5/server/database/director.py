import schema
import defines as d

def handle_create_director(name : str) -> d.ReturnCodes:
    new_director = schema.Directors(
        name=name
    )

    new_director.save()

    print(f"Created new director with ID {new_director.id}")

    return d.ReturnCodes.SUCCESS.value

def handle_read_director_by_id(record_id: int) -> list:
    director_id = record_id
    print(f"Reading director with ID: {director_id}")
    if director_id == d.WILDCARD_ID:
        directors = schema.Directors.select()
    else:
        directors = schema.Directors.select().where(schema.Directors.id == director_id)

    directors_list = [
        {
            "id": director.id,
            "name": director.name,
        }
        for director in directors
    ]

    if len(directors_list) == 0:
        print("Could not read directors")
        return [d.ReturnCodes.ERROR.value]

    print(f"Read {len(directors_list)} directors from database.")

    return [d.ReturnCodes.SUCCESS.value, directors_list]

def handle_read_director_by_name(director_name : str) -> list:
    print(f"Reading director with name: {director_name}")
    dir_query = schema.Directors.select().where(schema.Directors.name == director_name)
    if len(dir_query) == 0:
        print("Could not read director")
        return [d.ReturnCodes.ERROR.value]
    
    director = {}
    director['id'] = dir_query[0].id
    director['name'] = dir_query[0].name

    print(f"Read director with name {director_name} from database.")

    return [d.ReturnCodes.SUCCESS.value, director]

def handle_delete_director(record_id: int) -> d.ReturnCodes:
    print(f"Deleting director with ID: {record_id}")
    director = schema.Directors.get_by_id(record_id)
    if not director:
        print(f"No director with ID {record_id} found.")
        return d.ReturnCodes.ERROR.value

    director.delete_instance()
    print(f"Deleted director with ID: {record_id}")

    return d.ReturnCodes.SUCCESS.value    

def handle_update_director(record_id: int, new_name : str) -> d.ReturnCodes: 
    director = schema.Directors.get_by_id(record_id)
    if not director:
        print(f"No director with ID {record_id} found.")
        return d.ReturnCodes.ERROR.value

    director.name = new_name
    director.save()
    
    return d.ReturnCodes.SUCCESS.value
