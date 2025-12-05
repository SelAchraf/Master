#include "Classe.h"
#include <string.h>
#include <omnetpp.h>

Define_Module(gen);
Define_Module(attente);
Define_Module(server);

void gen::initialize()
{
    cMessage *msg = new cMessage();
    scheduleAt(simTime(), msg);
}

void gen::handleMessage(cMessage *msg)
{
    cMessage *msgk = new cMessage();
    msgk->setName("new");
    send(msgk, "out");
    scheduleAt(simTime() + exponential(1/0.25), new cMessage("new"));
    EV << "generate new message at " << simTime() << endl;
}

void attente::initialize()
{
    EV << getName() << "the queue is ready to save objects " << simTime() << endl;
}

void attente::handleMessage(cMessage *msg)
{
    if (strcmp(msg->getName(), "new") == 0){
        EV << "queue got a message to save At " << simTime() << endl;
        msg->setTimestamp(simTime());
        queue.insert(msg);
        EV << "the queue length become " << queue.length() << endl;
    }
    else if (strcmp(msg->getName(), "sch") == 0){
        EV << "Serveur: Request Message from Queue At " << simTime() << endl;
        if(!queue.isEmpty()){
            cMessage *m;
            m = (cMessage *)queue.pop();
            EV << "------------------------------------------------";
            EV << "Le temps d'attente du message " << m->getId() << " est " << simTime() - m->getTimestamp() << endl;
            send(m, "out");
        }
        else{
            EV << "Queue is empty" << endl;
        }
        scheduleAt(simTime() + exponential(1/0.08), new cMessage("sch"));
    }
}

void server::initialize()
{
    EV << getName() << "Serveur: I'am waiting for a message" << simTime() << endl;
    cMessage *msgk = new cMessage();
    msgk->setName("sch");
    sendDelayed(msgk,1 , "out");
}

void server::handleMessage(cMessage *msg)
{
    simtime_t sendt = msg->getCreationTime();
    simtime_t arrival = msg->getCreationTime();
    EV << "Le message (Job) " << msg->getId() << " a ete genere at " << sendt << endl;
    EV << "Le temps de debut de service du job " << msg->getId() << " est " << arrival << endl;
    double temps_service = exponential(1/0.08);
    EV << "Le temps de sejour du job " << msg->getId() << " est " << (arrival + temps_service) - sendt << " Avec un temps de service de " << temps_service << endl;
    delete msg;
}
