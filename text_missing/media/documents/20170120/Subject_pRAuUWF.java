package com.company.utils;

/**
 * Created by Melisa AM on 18.12.2016.
 */

public interface Subject {

        public void registerObserver(Observer observer);

        public void removeObserver(Observer observer);

        public void notifyObservers();

        public void notifyObservers(String designName, String typeOfChange);
}
