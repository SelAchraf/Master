import org.omg.CORBA.Object;
import javax.naming.Context;
import javax.naming.InitialContext;
import java.util.Hashtable;
import HelloApp.Hello;
import HelloApp.HelloHelper;

public class HelloClient {
    static Hello helloImplstub;

    public static void main(String[] args) {
        try {
            // Configure JNDI properties for CORBA Naming Service
            Hashtable<String, String> env = new Hashtable<>();
            env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.cosnaming.CNCtxFactory");
            env.put(Context.PROVIDER_URL, "iiop://localhost:1050");
            Context ctx = new InitialContext(env);

            org.omg.CORBA.Object objRef = (Object) ctx.lookup("RSI2020");

            // resolve the Object Reference in Naming:
            helloImplstub = HelloHelper.narrow(objRef);

            // juste pour voir de quoi a l’air la référence:
            System.out.println("On a obtenu un gestionnare pour le serveur d'objet " + helloImplstub);
            
            // l’appel de la méthode distante:
            System.out.println(helloImplstub.sayHello());
//            helloImplstub.shutdown();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}