import config
import cmd
import send_coin
import threading
import urllib
import get_db
import operator
import decimal

class sc(cmd.Cmd):
    prompt = "ShaShell$ "
    intro = "Welcome to the Shacoin shell, type `help` to get started."
    def do_send(self, line):
        line = line.split()
        try:
            to = line[0]
            amount = line[1]
        except:
            self.do_help(None)
        else:
            print "Coins are being sent"
            threading.Thread(target=send_coin.send, args=(to, amount)).start()
    
    def do_check(self, lines):
        get_db.send()

    def do_totalcoins(self, line):
        coin = config.db.find("coins", "all")
        if not coin:
            coin = 0
        else:
            coin = len(coin)
        print "There are "+str(coin)+" coins in existence."

    def do_coins(self, line):
        addr = config.wallet.find("data", "all")[0]
        addr = addr['address']
        coins = config.db.find("coins", {"address":addr})
        c = 0
        if not coins:
            c = 0
        else:
            for diff in coins: 
                diff = diff['difficulty']
                c += 1*10**(-12+diff)
            if "e" in str(c):
                c = str(c).split("e-")
                om = int(c[1])-1
                zeros = "0"*int(om)
                c = "0."+zeros+c[0].replace(".", '')
        print "You have "+str(c)+" coins."

    def do_addr(self, lines):
        addr = config.wallet.find("data", "all")[0]['address']
        print "Your address is: "+addr

    def do_transactions(self, line):
        line = line.split()
        if not line:
            self.do_help(None)
        else:
            data = config.db.find("transactions", {"from":line})
            if not data:
                print "No transactions have been made from this address."
            else:
                for x in data:
                    a = """
                        ID: {0}
                        To: {1}
                        Amount: {2}

                    """.format(x['transid'], x['to'], x['amount'])
                    print a


    def do_update(self, line):
        files = {
            "check_coin.py":"https://raw.github.com/Max00355/ShaCoin/master/check_coin.py",
            "coin_count.py":"https://raw.github.com/Max00355/ShaCoin/master/coin_count.py",
            "config.py":"https://raw.github.com/Max00355/ShaCoin/master/config.py",
            "get_db.py":"https://raw.github.com/Max00355/ShaCoin/master/get_db.py",
            "get_difficulty.py":"https://raw.github.com/Max00355/ShaCoin/master/get_difficulty.py",
            "get_nodes.py":"https://raw.github.com/Max00355/ShaCoin/master/get_nodes.py",
            "get_version.py":"https://raw.github.com/Max00355/ShaCoin/master/get_version.py",
            "landerdb.py":"https://raw.github.com/Max00355/ShaCoin/master/landerdb.py",
            "miner.py":"https://raw.github.com/Max00355/ShaCoin/master/miner.py",
            "register.py":"https://raw.github.com/Max00355/ShaCoin/master/register.py",
            "send_coin.py":"https://raw.github.com/Max00355/ShaCoin/master/send_coin.py",
            "send_command.py":"https://raw.github.com/Max00355/ShaCoin/master/send_command.py",
            "shell.py":"https://raw.github.com/Max00355/ShaCoin/master/shell.py",
            "shacoin.py":"https://raw.github.com/Max00355/ShaCoin/master/shacoin.py",
            
        }

        for x in files:
            print "Updating: "+x
            with open(x,'wb') as file:
                file.write(urllib.urlopen(files[x]).read())

    def do_stats(self, line):
        coins = config.db.find("coins", "all")
        trans = config.db.find("transactions","all")
        
        if not coins or not trans:
            print "Error working out stats"
        else:
            total = len(coins)
            coincounts = {}
            recievercounts = {}
            sendercounts = {}

            for coin in coins:
                try:
                    coincounts[coin['address']] += 1
                except:
                    if coin.has_key('address'):
                        coincounts[coin['address']] = 1
            for tran in trans:
                try:
                    recievercounts[tran['to']] += tran['amount']
                    sendercounts[tran['from']] += tran['amount']
                except:
                    recievercounts[tran['to']] = tran['amount']
                    sendercounts[tran['from']] = tran['amount']

            print "\nAddress".ljust(52),"Amt".ljust(len(str(total))),"%","\n","-"*63
            for address,count in sorted(coincounts.iteritems(), key=operator.itemgetter(1), reverse=True):
                print '%s %s %.2f%%'%(address.ljust(51), str(count).ljust(len(str(total))), (float(count)/float(total))*100)

            print "\nReceivers".ljust(52),"Trans Count","\n","-"*63
            for to,count in sorted(recievercounts.iteritems(), key=operator.itemgetter(1), reverse=True):
                print to.ljust(51),count

            print "\nSenders".ljust(52),"Trans Count","\n","-"*63
            for to,count in sorted(sendercounts.iteritems(), key=operator.itemgetter(1), reverse=True):
                print to.ljust(51),count
    
    def do_help(self, line):
        print """
            
            Welcome to the ShaCoin shell

            send <to> <amount> - Send coins to an address
            coins - Shows the amount of coins you currently own
            totalcoins - Shows total coins on the network
            transactions <addr> - Shows transactions made from an address
            update - Updates the source code
            addr - Displays your address
            check - Updates db.db manually. Useful when expecting payments
            stats - Get basic % counts and transaction info

        """

if __name__ == "__main__":
    sc().cmdloop()
