import java.util.ArrayList;
import java.util.ArrayList;
import java.util.Arrays;

//package com.example.demo_prac.HelloApplication.Parameters; // Uncomment this if you're using a package

public class Food {  // Renamed to follow Java class naming conventions
    public static void main(String[] args) {
        /* ArrayList<String> foodList = new ArrayList<>(); // Renamed for clarity

        foodList.add("Pizza");   // Capitalized for consistency
        foodList.add("Burger");
        foodList.add("Junk Food"); // Changed "junk" to "Junk Food" for clarity
        foodList.add("Meat pie");

        // Print all items
        System.out.println("Food List:");
        for (String item : foodList){
            System.out.println(item);
        }
        for (int i=0;i<foodList.size();i++){
            System.out.println(foodList.get(i));
        } */
      String[] friendslist = {"John", "Doe", "Jane", "Smith", "Jane", "Harry"};
      ArrayList<String> FriendsArrayList = new ArrayList<>(Arrays.asList("John", "Doe", "Jane", "Smith", "Jane", "Harry"));
      FriendsArrayList.add("jacques");
      FriendsArrayList.remove(1);
      friendslist[2]="Jacques";
      System.out.println(friendslist[2]);
      System.out.println(FriendsArrayList.get(5)); 
    }
}