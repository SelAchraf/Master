simple gen
{
    parameters:
        double meanInterArrival @unit(s) = default(4s);
    gates:
        output out;
}

simple attente
{
    parameters:
        double serviceMean @unit(s) = default(12s);
    gates:
        input in[];       // reçoit jobs et READY
        output out[3];    // un output pour chaque serveur
}

simple server
{
    parameters:
        double serviceMean @unit(s) = default(12s);
        int serverId;     // ID du serveur pour READY
    gates:
        input in;
        output out;       // renvoie "ready" vers File
}

network MM1
{
    @display("bgb=600,400");

    submodules:
        GEN: gen {
            @display("p=60,150;i=block/source");
        }

        File: attente {
            @display("p=170,241.5;i=block/queue");
        }

        serveur1: server {
            @display("p=369,150;i=block/sink");
            serverId = 0;
        }

        serveur2: server {
            @display("p=342,73;i=block/sink");
            serverId = 1;
        }

        serveur3: server {
            @display("p=369,234;i=block/sink");
            serverId = 2;
        }

    connections allowunconnected:

        // GEN → File
        GEN.out --> File.in++;

        // File → serveurs
        File.out[0] --> serveur1.in;
        File.out[1] --> serveur2.in;
        File.out[2] --> serveur3.in;

        // serveurs → File (READY)
        serveur1.out --> File.in++;
        serveur2.out --> File.in++;
        serveur3.out --> File.in++;
}
