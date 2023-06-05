import Levenshtein

def if_simmilar(response, template, similarity_threshold = 3):
    # response is a string
    # template is a list
    similarities = [Levenshtein.distance(response.lower(), word) for word in template]

    if any(similarity <= similarity_threshold for similarity in similarities):
        return True
    else:
        return False

    