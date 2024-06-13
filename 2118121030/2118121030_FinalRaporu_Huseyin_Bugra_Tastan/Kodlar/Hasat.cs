using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Hasat : MonoBehaviour
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
        Envanter.woodCount += 1;
        Envanter.hungerCount -= 25;
        Envanter.hungerCount = Mathf.Clamp(Envanter.hungerCount, 0, 100);

        
    }
}
