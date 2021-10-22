import datetime
import atexit

from datetime import timedelta

import rx
from rx import operators as ops

from influxdb_client import InfluxDBClient, WriteApi, WriteOptions

from Novra300 import Novra300

from config import NOVRA_HOST, NOVRA_PASSWORD, INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

VERIFY_SSL=True


def on_exit(db_client: InfluxDBClient, write_api: WriteApi):
    """Close clients after terminate a script.

    :param db_client: InfluxDB client
    :param write_api: WriteApi
    :return: nothing
    """
    write_api.close()
    db_client.close()


def novra_status(modem: Novra300):

    _status = modem.get_status()

    this_status = {}
    this_status["STATUS_TIMESTAMP"] = datetime.datetime.strptime(_status["STATUS_TIMESTAMP"], "%Y/%m/%d %H:%M:%S.%f")
    this_status["SIGNAL_STRENGTH_AS_DBM"] = int(_status["SIGNAL_STRENGTH_AS_DBM"])
    this_status["SIGNAL_LOCKED"] = _status["SIGNAL_LOCK"]=="Locked"
    this_status["DATA_LOCKED"] = _status["DATA_LOCK"]=="Locked"
    this_status["VBER"] = float(_status["VBER"])
    this_status["PER"] = float(_status["PER"])
    this_status["UNCORRECTABLES"] = int(_status["UNCORRECTABLES"])
    this_status["CARRIER_TO_NOISE"] = float(_status["CARRIER_TO_NOISE"])
    this_status["PID_COUNT"] = int(_status["PID_COUNT"])
    this_status["DVB_ACCEPTED"] = int(_status["DVB_ACCEPTED"])
    this_status["TOTAL_DVB_PACKETS_ACCEPTED"] = int(_status["TOTAL_DVB_PACKETS_ACCEPTED"])
    this_status["TOTAL_UNCORRECTABLE_TS_PACKETS"] = int(_status["TOTAL_UNCORRECTABLE_TS_PACKETS"])
    this_status["ETHERNET_TRANSMIT"] = int(_status["ETHERNET_TRANSMIT"])
    this_status["ETHERNET_RECEIVE"] = int(_status["ETHERNET_RECEIVE"])
    this_status["ETHERNET_PACKET_DROPPED"] = int(_status["ETHERNET_PACKET_DROPPED"])
    this_status["ETHERNET_RECEIVE_ERROR"] = int(_status["ETHERNET_RECEIVE_ERROR"])
    this_status["TOTAL_ETHERNET_PACKETS_OUT"] = int(_status["TOTAL_ETHERNET_PACKETS_OUT"])
    this_status["DVB_SCRAMBLED"] = int(_status["DVB_SCRAMBLED"])
    this_status["DVB_CLEAR"] = int(_status["DVB_CLEAR"])
    this_status["RECEIVER_MAC"] = _status["RECEIVER_MAC"]

    return this_status


def line_protocol_novra(novra_status):
    return (
        f"novra_status,modem={novra_status['RECEIVER_MAC']} "
        f"signal_strength_dbm={novra_status['SIGNAL_STRENGTH_AS_DBM']},"
        f"signal_locked={novra_status['SIGNAL_LOCKED']},"
        f"data_locked={novra_status['DATA_LOCKED']},"
        f"vber={novra_status['VBER']},"
        f"per={novra_status['PER']},"
        f"uncorrectable={novra_status['UNCORRECTABLES']},"
        f"carrier_to_noise={novra_status['CARRIER_TO_NOISE']},"
        f"pid_count={novra_status['PID_COUNT']},"
        f"dvb_accepted={novra_status['DVB_ACCEPTED']},"
        f"dvb_accepted_total={novra_status['TOTAL_DVB_PACKETS_ACCEPTED']},"
        f"uncorrectable_ts_packets={novra_status['TOTAL_UNCORRECTABLE_TS_PACKETS']},"
        f"ethernet_tx={novra_status['ETHERNET_TRANSMIT']},"
        f"ethernet_rx={novra_status['ETHERNET_RECEIVE']},"
        f"ethernet_dropped={novra_status['ETHERNET_PACKET_DROPPED']},"
        f"ethernet_error={novra_status['ETHERNET_RECEIVE_ERROR']},"
        f"ethernet_tx_total={novra_status['TOTAL_ETHERNET_PACKETS_OUT']},"
        f"dvb_scrambled_total={novra_status['DVB_SCRAMBLED']},"
        f"dvb_clear_total={novra_status['DVB_CLEAR']}"
        #f" {int(novra_status['STATUS_TIMESTAMP'].timestamp()*1e9)}"
    )


modem = Novra300(host=NOVRA_HOST, password=NOVRA_PASSWORD)

data = rx\
    .interval(period=timedelta(seconds=10))\
    .pipe(
        ops.map(lambda t: novra_status(modem)),
        ops.retry(),
        ops.map(lambda novra_status: line_protocol_novra(novra_status))
        )

_db_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG, debug=False, verify_ssl=VERIFY_SSL)

_write_api = _db_client.write_api(write_options=WriteOptions(batch_size=1))
_write_api.write(bucket=INFLUXDB_BUCKET, record=data)

atexit.register(on_exit, _db_client, _write_api)

input()