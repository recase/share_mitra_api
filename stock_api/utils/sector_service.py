from ..models import Sector
from ..serializers import SectorSerializer
from django.db import transaction
import datetime


def updateSectors(sectors_data):
    sector_list = []
    init = datetime.datetime.now()
    # list(Sector.objects.value('name')) --> return list
    sectors = Sector.objects.all().values('name')

    for sector in sectors_data:
        if {'name': sector['sectorDescription']} not in sectors.iterator():
            sec = Sector(name=sector['sectorDescription'],
                         regulatory_body=sector['regulatoryBody'])

            sector_list.append(sec)

    try:
        Sector.objects.bulk_create(
            sector_list, batch_size=100, ignore_conflicts=True)
    except Exception as e:
        print('error')
        print(e)

    fin = datetime.datetime.now()
    print(f'time: {fin - init}')
