#include "Server.h"

Define_Module(Server);

void Server::initialize()
{
    mu = par("mu");
    currentPacket = nullptr;

    waitingTimeVec.setName("waitingTime");
    sojournTimeVec.setName("sojournTime");

    totalCustomers = 0;
    totalWaitingTime = 0;
    totalSojournTime = 0;
}

void Server::handleMessage(cMessage *msg)
{
    if (msg->isSelfMessage()) {
        // ✅ Fin de service
        simtime_t arrivalTime = currentPacket->getTimestamp();
        simtime_t sojournTime = simTime() - arrivalTime;

        sojournTimeVec.record(sojournTime.dbl());
        totalSojournTime += sojournTime.dbl();

        int deviceId = currentPacket->par("deviceId");
        EV << "Server: Completed service for packet from Device " << deviceId
           << " (sojourn time: " << sojournTime << ")\n";

        delete currentPacket;
        currentPacket = nullptr;
        delete msg;

        // ✅ Notifier la queue que le serveur est libre
        cMessage *readyMsg = new cMessage("serverReady");
        send(readyMsg, "toQueue");

        EV << "Server: Sent 'serverReady' signal to Queue\n";
    }
    else {
        // ✅ Nouveau paquet de la queue
        totalCustomers++;
        currentPacket = msg;

        simtime_t arrivalTime = msg->getTimestamp();
        simtime_t waitingTime = simTime() - arrivalTime;

        waitingTimeVec.record(waitingTime.dbl());
        totalWaitingTime += waitingTime.dbl();

        int deviceId = msg->par("deviceId");
        EV << "Server: Starting service for packet from Device " << deviceId
           << " (waiting time: " << waitingTime << ")\n";

        // ✅ Planifier fin de service
        double serviceTime = exponential(1.0/mu);
        cMessage *endServiceMsg = new cMessage("endService");
        scheduleAt(simTime() + serviceTime, endServiceMsg);
    }
}

void Server::finish()
{
    if (currentPacket != nullptr) {
        delete currentPacket;
    }

    if (totalCustomers > 0) {
        double avgWaitingTime = totalWaitingTime / totalCustomers;
        double avgSojournTime = totalSojournTime / totalCustomers;

        EV << "\n=== Server Statistics ===\n";
        EV << "Total customers served: " << totalCustomers << "\n";
        EV << "Average waiting time: " << avgWaitingTime << " seconds\n";
        EV << "Average sojourn time: " << avgSojournTime << " seconds\n";

        recordScalar("totalCustomers", totalCustomers);
        recordScalar("avgWaitingTime", avgWaitingTime);
        recordScalar("avgSojournTime", avgSojournTime);
    }
}
