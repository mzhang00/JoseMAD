import datetime, subprocess

print("Please enter your name:")
print("Format: firstnameL")
name = input()

print("\n")
print("Please enter your update:")
update = input()

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

devlogFile = open("devlog.txt", "a")

devlogFile.write("\n" + name + " -- " + timestamp + "\n")
devlogFile.write(update+"\n")

devlogFile.close()

subprocess.run(['git', 'add', '-A'])
err = subprocess.run(['git', 'pull'])
# if err != 0:
#     subprocess.run(['git','stash'])
#     subprocess.run(['git', 'pull'])
#     subprocess.run(['git', 'stash', 'pop'])
#     print("FIX THE DAMN MERGE CONFLICTS")
# else:
subprocess.run(['git', 'commit', '-m', update])
subprocess.run(['git', 'push'])
