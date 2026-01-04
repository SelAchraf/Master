#include "Device.h"

Define_Module(Device);

void Device::initialize()
{
    lambda = par("lambda");
    groupSizeP = par("groupSizeP");
    deviceId = getIndex();  // ID du device (0-9)

    // Planifier première arrivée
    generateMsg = new cMessage("generate");
    scheduleAt(exponential(1.0/lambda), generateMsg);
}

void Device::handleMessage(cMessage *msg)
{
    // Générer un groupe de clients
    int groupSize = generateGroupSize();

    EV << "Device " << deviceId << " at time " << simTime()
       << ": Sending group of " << groupSize << " packets\n";

    // Envoyer chaque paquet du groupe vers la file d'attente
    for (int i = 0; i < groupSize; i++) {
        cMessage *packet = new cMessage("packet");
        packet->setTimestamp(simTime());  // Temps d'arrivée

        // Ajouter info sur le device source
        packet->addPar("deviceId") = deviceId;

        send(packet, "out");
    }

    // Planifier prochaine arrivée
    scheduleAt(simTime() + exponential(1.0/lambda), generateMsg);
}

int Device::generateGroupSize()
{
    // Distribution géométrique
    double u = uniform(0, 1);
    int size = (int)ceil(log(1 - u) / log(1 - groupSizeP));
    return (size > 0) ? size : 1;
}
