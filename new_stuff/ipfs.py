from pinatapy import PinataPy
from blockfrost import BlockFrostIPFS, ApiError

def upload_pinata_files(api_key, api_secret, files):
    if not isinstance(files, list):
        raise ValueError('The list of files provided for IPFS upload is not a list.')
    pinata = PinataPy(api_key, api_secret)

    auth = pinata.test_authentication()
    if 'message' in auth.keys():
        if auth['message'] == 'Congratulations! You are communicating with the Pinata API!':
            file_ipfs = {}
            for file in files:
                try:
                    result = pinata.pin_file_to_ipfs(file)
                    file_ipfs[file] = result['IpfsHash']
                except:
                    file_ipfs[file] = False
        else:
            raise ValueError('API key and or secret is invalid')
    else:
        raise ValueError('API key and or secret is invalid')
    return file_ipfs

def remove_pinata_files(api_key, api_secret, hashes):
    if not isinstance(hashes, list):
        raise ValueError('The list of hashes provided for IPFS removal is not a list.')
    pinata = PinataPy(api_key, api_secret)

    auth = pinata.test_authentication()
    if 'message' in auth.keys():
        if auth['message'] == 'Congratulations! You are communicating with the Pinata API!':
            for hash in hashes:
                file_ipfs = {}
                result = pinata.remove_pin_from_ipfs(hash)
                if 'message' in result.keys():
                    if result['message'] == 'Removed':
                        file_ipfs[hash] = True
                    else:
                        file_ipfs[hash] = False
                else:
                    file_ipfs[hash] = False
        else:
            raise ValueError('API key and or secret is invalid')
    else:
        raise ValueError('API key and or secret is invalid')
    return file_ipfs
    
def upload_blockfrost_files(api_key, files):
    if not isinstance(hashes, list):
        raise ValueError('The list of files provided for IPFS upload is not a list.')

    ipfs = BlockFrostIPFS(project_id=api_key)

    file_ipfs = {}
    for file in files:
        try:
            ipfs_object = ipfs.add(file)
            file_ipfs[file] = ipfs_object.ipfs_hash
        except:
            file_ipfs[file] = False
    return file_ipfs

def remove_blockfrost_files(api_key, hashes):
    if not isinstance(hashes, list):
        raise ValueError('The list of hashes provided for IPFS removal is not a list.')

    ipfs = BlockFrostIPFS(project_id=api_key)
    # Check if key is correct

    file_ipfs = {}
    for hash in hashes:
        try:
            ipfs_object = ipfs.pined_object_remove(hash)
            file_ipfs[hash] = True
        except:
            file_ipfs[hash] = False
            
    return file_ipfs

api_key = ''
api_secret = ''

print(upload_pinata_files(api_key, api_secret, ['C:\\Users\\tomdc\\Documents\\cardano\\metadata\\testing123.txt']))
print(remove_pinata_files(api_key, api_secret, ['QmQFmeH7Sc5viKfjB9ZzDr4fbPmHrDPLGpqGyryjCwLXMH']))




