using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ates_yakma : MonoBehaviour
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
        if (Envanter.woodCount >= 1 && Envanter.camphealthCount>=30)
        {
            Envanter.woodCount -= 1;
        Envanter.camphealthCount += 25;
        Envanter.camphealthCount = Mathf.Clamp(Envanter.camphealthCount, 0, 100);
        }

        if (Envanter.woodCount < 0)
        {
            Envanter.woodCount = 0;
        }

        if(Envanter.camphealthCount<30 && Envanter.stoneCount>=1)
        {
            Envanter.stoneCount -= 1;
            Envanter.camphealthCount += 25;
            Envanter.camphealthCount = Mathf.Clamp(Envanter.camphealthCount, 0, 100);
        }
        if (Envanter.stoneCount < 0)
        {
            Envanter.stoneCount = 0;
        }
    }
}
