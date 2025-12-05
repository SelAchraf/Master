#include "Classe.h"
#include <omnetpp.h>
#include <string>

using namespace omnetpp;

Define_Module(gen);
void gen::handleMessage(cMessage *msg)
{
    cMessage *job = new cMessage("new");
    send(job, "out");
    scheduleAt(simTime() + exponential(meanInterArrival), new cMessage("new"));
    EV << "[GEN] Generated job at " << simTime() << endl;
    delete msg;
}

Define_Module(attente);
Define_Module(server);

// ------------------------ GENERATOR ------------------------
void gen::initialize()
{
    meanInterArrival = par("meanInterArrival").doubleValue();
    scheduleAt(simTime(), new cMessage("new"));
}

// ------------------------ FILE (attente) ------------------------
void attente::initialize()
{
    int nServers = gateSize("out");
    serverFree.assign(nServers, true); // tous les serveurs libres au début

    queueLengthVec.setName("queueLength");
    lifeTimeVec.setName("lifeTime");
    EV << "[FILE] initialized at " << simTime() << endl;
}

void attente::handleMessage(cMessage *msg)
{
    const char *name = msg->getName();

    // ---------- NEW job ----------
    if (strcmp(name, "new") == 0)
    {
        msg->setTimestamp(simTime());
        queue.insert(msg);
        queueLengthVec.record(queue.length());
        EV << "[FILE] Received NEW, queue size = " << queue.length() << endl;

        // envoi vers premier serveur libre
        for (int i = 0; i < (int)serverFree.size(); ++i)
        {
            if (serverFree[i])
            {
                cMessage *job = (cMessage *)queue.pop();
                serverFree[i] = false;
                send(job, "out", i); // envoi via gate vector
                queueLengthVec.record(queue.length());
                EV << "[FILE] Sent job " << job->getId() << " to server " << i << endl;
                break;
            }
        }
    }
    // ---------- READY from server ----------
    else if (strcmp(name, "ready") == 0)
    {
        int serverIndex = msg->getKind();
        EV << "[FILE] Received READY from server " << serverIndex << " at " << simTime() << endl;

        if (!queue.isEmpty())
        {
            cMessage *job = (cMessage *)queue.pop();
            send(job, "out", serverIndex);
            queueLengthVec.record(queue.length());
            EV << "[FILE] Sent job " << job->getId() << " to server " << serverIndex << endl;
        }
        else
        {
            if (serverIndex >= 0 && serverIndex < (int)serverFree.size())
                serverFree[serverIndex] = true;
        }
        delete msg;
    }
    else
    {
        EV << "[FILE] Unexpected message " << name << endl;
        delete msg;
    }
}

// ------------------------ SERVER ------------------------
void server::initialize()
{
    serviceMean = par("serviceMean").doubleValue();
    serverId = par("serverId").intValue();

    lifeTimeVec.setName(("lifeTime_server" + std::to_string(serverId)).c_str());

    // envoi READY initial
    cMessage *ready = new cMessage("ready");
    ready->setKind(serverId);
    send(ready, "out");
    EV << "[SERVER" << serverId << "] Initialized and sent READY at " << simTime() << endl;
}

void server::handleMessage(cMessage *msg)
{
    const char *name = msg->getName();
    if (strcmp(name, "new") == 0)
    {
        double ts = exponential(serviceMean);
        simtime_t genTime = msg->getCreationTime();

        EV << "[SERVER" << serverId << "] Received job " << msg->getId()
           << " at " << simTime() << ", service = " << ts << endl;

        // envoyer READY après service
        cMessage *ready = new cMessage("ready");
        ready->setKind(serverId);
        sendDelayed(ready, ts, "out");

        // enregistrer temps de séjour
        lifeTimeVec.record(simTime() - genTime + ts);

        delete msg;
    }
    else
    {
        EV << "[SERVER" << serverId << "] Unexpected msg " << name << endl;
        delete msg;
    }
}
