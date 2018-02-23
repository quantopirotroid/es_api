### Requirements:
 * docker-compose
 * docker engine 17.09.0+

### Usage
Define your server settings in `.env` and `config.py` files and use commands bellow:

```
git clone https://github.com/quantopirotroid/es_api
cd es_api
./install.sh
```

### API
Headers requared:
* Content-Type: application/json
* X-DB-api-auth-token: very_srong_token - __defined in__ `config.py`

***/api/add*** method __POST__, fomat __json__
Fields:
* "index": "index name"
* "doc_type": "document type - just string, defines document"
* "id": "documen id"
* "body": "document body to insert in index"
Returns json:
* fields:
    * "created": "True"
    * "data": "body"
    * "id": "id"
    * "index": "index"
    * "doc_type": "doc_type"

***/api/get*** method __POST__, fomat __json__
Fields:
* "index": "index name"
* "doc_type": "document type - string, defines document"
* "id": "documen id"
Returns json:
* fields:
    * "body": "requestad data"
    * "id": "id"
    * "index": "index"
    * "doc_type": "doc_type"

***/api/search*** method __POST__, fomat __json__
Fields:
* "index": "index name"
* "doc_type": "document type - string, defines document"
* "id": "documen id"
Returns json:
* fields:
    * "body": "requestad data"
    * "id": "id"
    * "index": "index"
    * "doc_type": "doc_type"


### For example:

```
curl -X POST https://example.com/api/add -d \
'{
    "index": "literature",
    "doc_type": "classical",
    "id": "1",
    "body": {
             "countries": {
	                   "Russia": {
			              "P": {
				            "Pushkin": {
	                                                "first name": "Александр",
	                                                "second name": "Пушкин",
	                                                "works": {
	                                                          "prose": {
	                                                                    "1830": "Капитанская дочка",
	                                                                    "1833": "Дубровский",
	                                                     		    "1834": "Пиковая дама"
	                                                          },
	                                                          "poetry": {
					            	                 "1831": "Евгений Онегин",
					            	                 "1833": "Гусар"
	                                                          }
	                                                }
					    }
				      },
				      "D": {
				            "Davidov": {
	                                                "first name": "Денис",
	                                                "second name": "Давыдов",
	                                                "works": {
	                                                          "poetry": {
					            	                 "1817": "Песня старого гусара",
					            	                 "1832": "Голодный пёс"
	                                                          }
	                                                }
					    }
				            
				            
				      }
	                   },
			   "USA": {
                                   "P": {
				         "Poe": {
				                 "first name": "Edgar",
				  	         "second name": "Poe",
					         "works": {
					                   "1845": "Raven"
					         }
				         }
				   }
			   }
	     }
    }
}' -H 'X-DB-api-auth-token: hfgdHHGKbfds765349hbdsH16' -H "Content-Type: application/json" -k | \
python -c "import sys;import codecs;[sys.stdout.write((codecs.unicode_escape_decode(i)[0])) for i in sys.stdin]
```

```
curl -X POST https://example.com/api/get -d \
'{
    "index": "literature",
    "doc_type": "classical",
    "id": "1"
}' -H 'X-DB-api-auth-token: hfgdHHGKbfds765349hbdsH16' -H "Content-Type: application/json" -k | \
python -c "import sys;import codecs;[sys.stdout.write((codecs.unicode_escape_decode(i)[0])) for i in sys.stdin]"
```

```
curl -X POST https://example.com/api/search-d \
'{
    "index": "literature",
    "doc_type": "classical",
    "text": "Давыдов"
}' -H 'X-DB-api-auth-token: hfgdHHGKbfds765349hbdsH16' -H "Content-Type: application/json" -k | \
python -c "import sys;import codecs;[sys.stdout.write((codecs.unicode_escape_decode(i)[0])) for i in sys.stdin]"
```

