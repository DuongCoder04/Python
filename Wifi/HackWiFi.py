import subprocess

# getting meta data
meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])

# decoding meta data
data = meta_data.decode('utf-8', errors="backslashreplace")

# splitting data by line by line
data = data.split('\n')

# creating a list of profiles
profiles = []

# traverse the data
for i in data:
    # find "All User Profile" in each item
    if "All User Profile" in i:
        # if found, split the item
        i = i.split(":")
        # item at index 1 will be the wifi name
        i = i[1].strip()  # Use strip() to remove leading/trailing whitespaces
        # appending the wifi name in the list
        profiles.append(i)

# printing heading
print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
print("----------------------------------------------")

# traversing the profiles
for i in profiles:
    try:
        # getting meta data with password using wifi name
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
        # decoding and splitting data line by line
        results = results.decode('utf-8', errors="backslashreplace")
        results = results.split('\n')
        # finding password from the result list
        results = [b.split(":")[1][1:-1].strip() for b in results if "Key Content" in b]
        # if there is password, it will print the password
        try:
            print("{:<30}| {:<}".format(i, results[0]))
        # else it will print blank in front of password
        except IndexError:
            print("{:<30}| {:<}".format(i, ""))
    except subprocess.CalledProcessError:
        print("Encoding Error Occurred")
