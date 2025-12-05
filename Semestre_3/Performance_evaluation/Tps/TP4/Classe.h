#ifndef CLASSE_H_
#define CLASSE_H_

#include <omnetpp.h>
#include <string>

using namespace omnetpp;

class gen : public cSimpleModule {
private:
    cMessage *generateEvent;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

class attente : public cSimpleModule {
private:
    cQueue queue;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

class server : public cSimpleModule {
private:
    cMessage *serviceEvent;
    cMessage *currentJob;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

#endif /* CLASSE_H_ */
