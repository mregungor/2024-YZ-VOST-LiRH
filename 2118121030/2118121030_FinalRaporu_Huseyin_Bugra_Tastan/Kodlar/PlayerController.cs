using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    Rigidbody rb;
    [SerializeField] float MoveSpeed=10;
    [SerializeField] float Jump=5;
    // Start is called before the first frame update
    void Start()
    {
        rb=GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        float horInput = Input.GetAxisRaw("Horizontal") * MoveSpeed;
        float verInput = Input.GetAxisRaw("Vertical") * MoveSpeed;

        rb.velocity = new Vector3(horInput, rb.velocity.y, verInput);

    if(Input.GetButtonDown("Jump")&&Mathf.Approximately(rb.velocity.y,0)) rb.velocity = new Vector3(rb.velocity.x,Jump,rb.velocity.z);
    transform.forward = new Vector3(rb.velocity.x,0,rb.velocity.z);
    }
}
