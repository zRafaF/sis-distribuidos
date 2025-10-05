class Movie():

    def __init__(self, movie_id, director_id, title, director_name, 
                length_minutes, gender, rating):
        self.id = movie_id
        self.director_id = director_id
        self.title = title 
        self.director_name = director_name
        self.length_minutes = length_minutes
        self.gender = gender
        self.rating = rating

# Necessary for remote object passing with Pyro5
def Movie_to_dict(mov:Movie):
    dicionario = {
        "__class__":"Movie.Movie",
        'id' : mov.id,
        'director_id' : mov.director_id,
        'title' : mov.title,
        'director_name' : mov.director_name,
        'length_minutes' : mov.length_minutes,
        'gender' : mov.gender,
        'rating' : mov.rating
    }
    return dicionario

# Necessary for remote object reception with Pyro5
def dict_to_Movie(classname, dicionario:dict):
    mov = Movie(dicionario["id"], dicionario["director_id"], 
                dicionario["title"],dicionario["director_name"],
                dicionario["length_minutes"],dicionario["gender"],
                dicionario["rating"])

    return mov
    
