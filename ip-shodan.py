import shodan
import sys

# Replace 'YOUR_API_KEY' with your actual Shodan API key
SHODAN_API_KEY = '<YOUR-SHODAN-KEY>'

def search_hostname(api_key, hostname):
    try:
        api = shodan.Shodan(api_key)
        query = f'hostname:"{hostname}"'
        results = api.search(query)

        ips = [result['ip_str'] for result in results['matches']]
        return ips
    except shodan.APIError as e:
        print('Error:', e)
        return []

def search_ssl(api_key, hostname):
    try:
        api = shodan.Shodan(api_key)
        query = f'ssl:"{hostname}"'
        results = api.search(query)

        ips = [result['ip_str'] for result in results['matches']]
        return ips
    except shodan.APIError as e:
        print('Error:', e)
        return []

def search_ssl_cert_cn(api_key, hostname):
    try:
        api = shodan.Shodan(api_key)
        query = f'ssl.cert.subject.CN:"{hostname}"'
        results = api.search(query)

        ips = [result['ip_str'] for result in results['matches']]
        return ips
    except shodan.APIError as e:
        print('Error:', e)
        return []

def format_and_save_ips(ips):
    with open('ips.txt', 'w') as file:
        for ip in sorted(set(ips)):
            print(ip)
            file.write(ip + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script_name.py website.com')
        sys.exit(1)

    hostname_to_search = sys.argv[1]
    hostname_ips = search_hostname(SHODAN_API_KEY, hostname_to_search)
    ssl_ips = search_ssl(SHODAN_API_KEY, hostname_to_search)
    ssl_cert_cn_ips = search_ssl_cert_cn(SHODAN_API_KEY, hostname_to_search)

    all_ips = hostname_ips + ssl_ips + ssl_cert_cn_ips
    print("IP Addresses:")
    format_and_save_ips(all_ips)
