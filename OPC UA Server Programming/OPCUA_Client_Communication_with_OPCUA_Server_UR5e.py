# This is OPC UA Client - Communication with UR5e OPC UA Server
import asyncio
import logging
import concurrent.futures
from asyncua import Client, ua

#logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Url for connection to UR5 with username and password (both have to be replaced with actual access data)
url_ur5 = "opc.tcp://192.168.158.34:4840"


# Client functions used to read and write variables from/to OPC UA Server in robot control

# Read single variable of nodeID, return this value
async def read_var(nodeID):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID)
        value = await node.read_value()
        return value


# Write single value to variable with nodeID
async def write_service(nodeID, value):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID)
        await node.write_value(value, ua.VariantType.Int32)


# Write single value to variable with nodeID
async def write_start(nodeID, value):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID)
        await node.write_value(value, ua.VariantType.Boolean)


# Write two values, here position represented by current id and dir value
async def write_pos(nodeID_id, nodeID_dir, id, dir):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID_id)
        await node.write_value(id, ua.VariantType.Int32)

        node = client.get_node(nodeID_dir)
        await node.write_value(dir, ua.VariantType.Int32)


# Read two values, here position represented by current id and dir value, return these values
async def read_pos(nodeID_id, nodeID_dir):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID_id)
        value_1 = await node.read_value()

        node = client.get_node(nodeID_dir)
        value_2 = await node.read_value()

        return [value_1, value_2]


async def main():
    while True:
        client = Client(url=url_ur5, timeout=60, watchdog_interval=60)
        try:
            # Running Client
            async with client:
                logger.info("Starting Client!")
        
            while True:
                await asyncio.sleep(0.5)
                await client.check_connection()
        except:
            _logger.warning("Reconnecting Client in 1 second")
            await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())