from ftplib import FTP
import glob, os

main_path = '/archive/data/'
actual_files_nc = set(map(lambda s: s.split('/')[-1],glob.glob(os.path.join(main_path, "*.nc"))))

print('[+] Conectado con el servidor FTP....')
ftp_main_path = '/pub/data/nccf/com/rtofs/prod/'
ftp = FTP('ftpprd.ncep.noaa.gov')
print(ftp.login())
print('[+] Conexion lista !')

print('[+] Listando carpetas a descargar ...')
ftp.cwd(ftp_main_path)
dir_2020 = ftp.nlst('*2020*')
print('[+] Las carpetas a descargar son: ',dir_2020)

print('[+] Listando archivos a descargar ...')
for _dir in dir_2020:
    ftp.cwd(ftp_main_path + _dir)
    files_nc  = ftp.nlst('*.nc')
    files_nc = set(files_nc) - actual_files_nc
    print('[+] La cantidad de archivos a descargar para la carpeta ',_dir, ' son ',len(files_nc) ,' archivos .nc')
    for file_nc in files_nc:
        with open(_dir+'.'+file_nc, 'wb') as f:
            print('[+] Descargando {}...'.format(file_nc))
            ftp.retrbinary('RETR %s' % file_nc, f.write)
    print('[+] Descarga lista para la carpeta ', _dir)

print('[+] Todas las escargs estan listas !')
print(ftp.quit())
print('[+] Adios...')