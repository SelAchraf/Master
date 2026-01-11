#ifndef QUEUE_H
#define QUEUE_H

#include <omnetpp.h>
#include <queue>

using namespace omnetpp;

class Queue : public cSimpleModule
{
private:
    std::queue<cMessage*> buffer;
    bool serverBusy;  // Suivre l'état du serveur

    // Statistiques
    cOutVector queueLengthVec;
    simtime_t lastEventTime;
    double areaUnderQueueLength;
    long totalArrivals;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
    void tryToSendToServer();  // Tenter d'envoyer au serveur
};

#endif
