import requests
import sys

def main():
    try:
        btc = float(sys.argv[1])
        usd = get_exchange_rate()*btc
        formatted = f"{usd:,.4f}"

        print(f"${formatted}")
        print("done")
    except IndexError:
        sys.exit("Missing command-line argument")
    except ValueError:
        sys.exit("Command-line argument is not a number")

def get_exchange_rate():

    try:
        r = requests.get('https://rest.coincap.io/v3/assets/bitcoin?apiKey=3dd3f7a7c8b3db78d0585f6d77eca0303227292aef5d9e28bc713980dff7290e')

        response_obj = r.json()

        return float(response_obj["data"]["priceUsd"])

    except requests.RequestException as e:
        print(e)


if __name__ == "__main__":
    main()
