using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class yemek_hasat : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    private void OnTriggerEnter(Collider other)
    {
        Envanter.foodCount += 1;
        Envanter.hungerCount += 25;
        Envanter.foodCount -= 1;
        

    }
}
