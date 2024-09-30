#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Client {
private:
    int client_id;
    string name;
    string surname;
    string phone_number;

public:
    Client(int id, string nm, string srn, string phone)
        : client_id(id), name(nm), surname(srn), phone_number(phone) {}

    string getName() const { return name; }
    void setName(const string& nm) { name = nm; }

    string getPhoneNumber() const { return phone_number; }
    void setPhoneNumber(const string& phone) { phone_number = phone; }

    void displayClientInfo() const {
        cout << "Client: " << name << " " << surname << ", Phone: " << phone_number << endl;
    }

    void updatePhoneNumber(const string& new_phone) {
        phone_number = new_phone;
        cout << "Phone number updated to: " << phone_number << endl;
    }
};

class Payment {
public:
    virtual void processPayment(double amount) const {
        cout << "Processing payment of $" << amount << endl;
    }
};

class Device {
private:
    int device_id;
    string type;
    string brand;

public:
    Device(int id, string tp, string brd)
        : device_id(id), type(tp), brand(brd) {}

    void displayDeviceInfo() const {
        cout << "Device: " << brand << " " << type << endl;
    }
};

class RepairApplication : public Client, public Device, public Payment {
private:
    int application_id;
    string status;
    double planned_price;

public:
    RepairApplication(int app_id, string stat, double price, int client_id, string name, string surname, string phone,
        int device_id, string type, string brand)
        : Client(client_id, name, surname, phone), Device(device_id, type, brand),
        application_id(app_id), status(stat), planned_price(price) {}

    void displayApplicationInfo() const {
        displayClientInfo();
        displayDeviceInfo();
        cout << "Application ID: " << application_id << ", Status: " << status
            << ", Planned Price: $" << planned_price << endl;
    }

    void processPayment(double amount) const override {
        cout << "Payment for repair application " << application_id << ": $" << amount << endl;
    }
};

class Worker : public Client {
private:
    int worker_id;
    string position;

public:
    Worker(int id, string nm, string srn, string phone, int w_id, string pos)
        : Client(id, nm, srn, phone), worker_id(w_id), position(pos) {}

    void displayWorkerInfo() const {
        displayClientInfo();
        cout << "Worker ID: " << worker_id << ", Position: " << position << endl;
    }

    void assignRepair(int application_id) {
        cout << "Worker assigned to repair application " << application_id << endl;
    }
};

int main() {
    Client client1(1, "John", "Doe", "123-456-789");
    client1.displayClientInfo();
    client1.updatePhoneNumber("987-654-321");

    Worker worker1(2, "Michael", "Smith", "987-654-123", 101, "Technician");
    worker1.displayWorkerInfo();

    RepairApplication app1(1001, "In Progress", 250.75, 1, "John", "Doe", "987-654-321", 2001, "Laptop", "Dell");
    app1.displayApplicationInfo();

    RepairApplication app2(1002, "Completed", 150.50, 3, "Alice", "Johnson", "555-123-456", 2002, "Phone", "Samsung");
    app2.displayApplicationInfo();

    app1.processPayment(250.75);
    app2.processPayment(150.50);

    worker1.assignRepair(1001);

    return 0;
}