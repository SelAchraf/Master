#include "Queue.h"

Define_Module(Queue);

void Queue::initialize()
{
    queueLengthVec.setName("queueLength");
    lastEventTime = 0;
    areaUnderQueueLength = 0;
    totalArrivals = 0;
    serverBusy = false;  // Serveur libre au début
}

void Queue::handleMessage(cMessage *msg)
{
    if (strcmp(msg->getName(), "serverReady") == 0) {
        // Le serveur est maintenant libre
        EV << "Queue: Server is now ready\n";

        serverBusy = false;
        delete msg;

        // Essayer d'envoyer le prochain paquet
        tryToSendToServer();
    }
    else {
        // Nouveau paquet d'un device
        totalArrivals++;

        int deviceId = msg->par("deviceId");
        EV << "Queue: Received packet from Device " << deviceId
           << " at time " << simTime() << "\n";

        // Mise à jour statistiques
        int oldQueueLength = buffer.size() + (serverBusy ? 1 : 0);
        areaUnderQueueLength += oldQueueLength * (simTime() - lastEventTime).dbl();
        lastEventTime = simTime();

        // Ajouter à la file
        buffer.push(msg);
        queueLengthVec.record(buffer.size() + (serverBusy ? 1 : 0));

        // Essayer d'envoyer au serveur
        tryToSendToServer();
    }
}

void Queue::tryToSendToServer()
{
    // Envoyer seulement si serveur libre ET file non vide
    if (!serverBusy && !buffer.empty()) {
        cMessage *packet = buffer.front();
        buffer.pop();

        int deviceId = packet->par("deviceId");
        EV << "Queue: Sending packet from Device " << deviceId
           << " to Server (queue length now: " << buffer.size() << ")\n";

        serverBusy = true;  // Marquer serveur comme occupé
        send(packet, "out");

        // Mise à jour statistiques
        queueLengthVec.record(buffer.size() + 1);
        areaUnderQueueLength += (buffer.size() + 1) * (simTime() - lastEventTime).dbl();
        lastEventTime = simTime();
    }
}

void Queue::finish()
{
    if (simTime() > 0) {
        double avgQueueLength = areaUnderQueueLength / simTime().dbl();

        EV << "\n=== Queue Statistics ===\n";
        EV << "Total arrivals: " << totalArrivals << "\n";
        EV << "Average queue length: " << avgQueueLength << "\n";
        EV << "Final queue size: " << buffer.size() << "\n";

        recordScalar("avgQueueLength", avgQueueLength);
        recordScalar("totalArrivals", totalArrivals);
        recordScalar("finalQueueSize", buffer.size());
    }
}
