#ifndef SERVER_H
#define SERVER_H

#include <omnetpp.h>

using namespace omnetpp;

class Server : public cSimpleModule
{
private:
    double mu;
    cMessage *currentPacket;  // Paquet en cours de service

    // Statistiques
    cOutVector waitingTimeVec;
    cOutVector sojournTimeVec;
    long totalCustomers;
    double totalWaitingTime;
    double totalSojournTime;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};

#endif
