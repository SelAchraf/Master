#ifndef CLASSE_H_
#define CLASSE_H_

#include <omnetpp.h>
#include <vector>

using namespace omnetpp;

class gen : public cSimpleModule {
  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    double meanInterArrival;
};

class attente : public cSimpleModule {
  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;

    cQueue queue;                        // FIFO storage for jobs
    std::vector<bool> serverFree;        // serverFree[i] = true if server i is free
    cOutVector queueLengthVec;           // queue length over time
    cOutVector lifeTimeVec;              // job lifetime (sojourn)
};

class server : public cSimpleModule {
  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;

    double serviceMean;
    int serverId;
    cOutVector lifeTimeVec;              // pour enregistrer le temps de séjour
};

#endif /* CLASSE_H_ */
