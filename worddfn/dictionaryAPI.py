# Help Create objects for different Dictionary API's.


class WordnikConfig:
    """Create objects for the wordnik api."""

    def __init__(self) -> None:
        self.url = ""
        self.headers = {}
        self.parameters = {}

    def show_api_obj(self) -> str:
        """Print the Object url, header and parameter. Simple put it display if the object is empty or not."""

        return f"Object contains:\nurl:{self.url}\nheaders:{self.headers}\nparameters:{self.parameters}"

    def headers_construct(self, accp: str, API_KEY: str) -> dict:
        """Build part of the HTTP request header.
        accp:        Accepts type: e.g. application/json
        API_KEY:     API KEY: uses an Wordnik API KEY.
        This method returns a dictionary"""

        return {
            "Accepts": accp,
            "api_key": API_KEY,
        }

    def parameters_construct(self, endPoint: str, *query: tuple[str]) -> dict:
        """Builds out the parameters for the HTTP request, returns a dictionary
        This method takes a wordnik api endpoint and optionaly can be pass a
        list of query varibles witch the api uses to get specific results."""

        # Create parameters use for calling the definitions endpoint.
        if endPoint == "definitions":
            limit: str = query[0]
            src: str = query[1]
            tag: str = query[2]

            parameters = {
                "limit": limit,
                "sourceDictionaries": src,
                "includeTags": tag,
            }

        # Create parameters use for calling the relatedWords endpoint.
        elif endPoint == "relatedWords":
            # Create parameters use for calling the relatedWords endpoint when exactly two query variable is pass.
            if len(query) == 2:
                word_relations: srt = query[0]
                limit_relations: srt = query[1]

                parameters = {
                    "relationshipTypes": word_relations,
                    "limitPerRelationshipType": limit_relations,
                }

            # Create parameters use for calling the relatedWords endpoint when exactly one query variable is pass.
            elif len(query) == 1:
                val = query[0]
                # Check to see if the querry have numbers in it.
                if val.isdecimal():
                    # print(type(val))  # test code
                    limit_relations: str = query[0]

                    parameters = {
                        "relationshipTypes": "verb-form",
                        "limitPerRelationshipType": limit_relations,
                    }

                # Check to see if the querry is compose of only string.
                elif val.isalpha():
                    # print(type(val))  # test code
                    word_relations: str = query[0]

                    parameters = {
                        "relationshipTypes": word_relations,
                        "limitPerRelationshipType": "5",
                    }

            else:  # Test code
                print("something wrong")  # Test code

        return parameters

    def url_construct(self, URL: str, word: str, endPoint: str) -> str:
        """Builds a full wordnik api URL to get results.
             URL:         the wordnik api base url.
             word:        a word to search in the dictionary for.
             endPoint:    the wordnik api endpoint.
        this nethod returns a string with the fully created wordnik api url."""

        url = f"{URL}{word}/{endPoint}"
        return url

    def api_construct(self, url: str, headers: dict, parameters: dict) -> None:
        """Assign elements to the created api object."""

        self.url = url
        self.headers = headers
        self.parameters = parameters


if __name__ == "__main__":
    print(f"Executing from {__name__}")
