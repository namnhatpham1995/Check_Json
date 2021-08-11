# Check_Json
 Validate Json request
## Installation

- Clone this repo:
	
	```
	$ git clone https://github.com/namnhatpham1995/Check_Json.git
	```

- Install the requirements:
	
	```
	pip install -r requirements.txt
	```

## Usage
- To run application, move to project folder and run:
	
	```
	$ python app.py
	```
 or
 	```
	$ python3 app.py
	```
## Test
- To test application, use Postman (https://web.postman.co/) (or any methods) to send Json request to the address  http://[computer's IP address]:5000/check_json \\
for example:\\
	```
             {
                "customerID":1,
                "customerName":"abc",
                "request_info":"ask questions",
                "remoteIP":"123.456.789"
             }
	```
