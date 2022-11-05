import argparse
from fabric import Connection


class RemoteMounter:
    def __init__(self, sourcepath, host, testpath, sshuser, userpass):
        self.__user = sshuser
        self.__host = host
        self.__testpath = testpath
        self.__userpass = userpass
        self.__sourcepath = sourcepath

    def mount(self):
        try:
            with Connection(host=self.__host, user=self.__user, connect_kwargs={'password': self.__userpass}) as c:
                c.sudo(f'losetup -fP {self.__sourcepath}', password=self.__userpass, hide=True)
                result = c.run(f'losetup -a | grep {self.__sourcepath}')
                res = result.stdout[:result.stdout.index(':')]
                c.sudo(f'mkdir -p {self.__testpath}', password=self.__userpass, hide=True)
                c.sudo(f'mount -o loop {res} {self.__testpath}', password=self.__userpass, hide=True)
                c.sudo(f'chmod 777 -R {self.__testpath}', password=self.__userpass, hide=True)
        except:
            print(f'')

    def umount(self):
        with Connection(host=self.__host, user=self.__user, connect_kwargs={'password': self.__userpass}) as c:
            result = c.run(f'losetup -a | grep {self.__sourcepath}')
            res = result.stdout[:result.stdout.index(':')]
            c.sudo(f'sync', password=self.__userpass, hide=True)
            c.sudo(f'umount {self.__testpath}', password=self.__userpass, hide=True)
            c.sudo(f'losetup -d {res}', password=self.__userpass, hide=True)


def parser_data():
    parser = argparse.ArgumentParser(description='(U)mount script')
    parser.add_argument('action', help="mount or umount")
    parser.add_argument('-n', dest='sourcepath', default='/home/marinara/testdataset.img')
    parser.add_argument('-t', dest='host', default='192.168.208.77')
    parser.add_argument('-w', dest='testpath', default='/media/sdx')
    parser.add_argument('-u', dest='sshuser', default='nadya')
    parser.add_argument('-p', dest='userpass', default='nadya')
    return parser.parse_args()


if __name__ == '__main__':
    args = parser_data()
    remote_mounter = RemoteMounter(args.sourcepath, args.host, args.testpath, args.sshuser, args.userpass)
    if args.action == 'mount':
        remote_mounter.mount()
    elif args.action == 'umount':
        remote_mounter.umount()
