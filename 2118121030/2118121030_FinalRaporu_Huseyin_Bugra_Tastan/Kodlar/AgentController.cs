using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgents;
using System;
using TMPro;

public class AgentController : Agent//Bu sýnýf, Agent sýnýfýndan türetilmiþ bir sýnýftýr. ML-Agents çerçevesindeki bir ajaný temsil eder.
{
    [SerializeField] private Transform target;//hedef
    [SerializeField] private Transform target1;//hedef
    [SerializeField] private Transform target2;//hedef
    [SerializeField] public TextMeshProUGUI rewardText;

    private Rigidbody rb;
    private float totalReward = 0f;
    public int i = 0;
    public float moveRotate;
    
    public override void Initialize()
    {
        rb= GetComponent<Rigidbody>();
        
    }

    public override void OnEpisodeBegin() //Bu metot, her eðitim bölümü (episode) baþladýðýnda çaðrýlýr. Ajanýn baþlangýç pozisyonunu ve hedef pozisyonunu sýfýrlar.
    {
        transform.localPosition = new Vector3(25.76f, 0.01f, 19.29f);
        

    }
    public override void CollectObservations(VectorSensor sensor)//Bu metot, ajanýn algýlarýný (gözlemlerini) toplar. Burada, ajanýn kendi pozisyonunu ve hedefin pozisyonunu toplar ve VectorSensor kullanarak sensor parametresine ekler.
    {
        sensor.AddObservation(transform.localPosition);
        sensor.AddObservation(target.localPosition);
        sensor.AddObservation(target1.localPosition);
        sensor.AddObservation(target2.localPosition);
    }
    public override void OnActionReceived(ActionBuffers actions)//Bu metot, ajanýn bir eylem aldýðýnda çaðrýlýr. Burada, ajanýn aldýðý eyleme göre hareket eder.
    {
        float moveSpeed = 2f;
        //Vector3 inputVector = Vector3.zero;
          moveRotate = actions.ContinuousActions[0];
         float moveForward = actions.ContinuousActions[1];
        rb.MovePosition(transform.position+transform.forward*moveForward*moveSpeed*Time.deltaTime);
        transform.Rotate(0f,moveRotate*moveSpeed,0f,Space.Self);

        //inputVector.x = actions.ContinuousActions[0];//ajanin x eksenindeki hareket inputVector un x bilesenine atanir
        //inputVector.z = actions.ContinuousActions[2];//ajanin z eksenindeki hareket inputVector un y bilesenine atanir

        //transform.localPosition += new Vector3(inputVector.x, 0, inputVector.z) * Time.deltaTime * moveSpeed;
    }

    public override void Heuristic(in ActionBuffers actionsOut)//Bu metot, ajanýn insan tarafýndan kontrol edildiði durumlarý simüle eder. Burada, ajanýn klavye giriþlerine göre eylemleri belirlenir.
    {
        ActionSegment<float> continuousActions = actionsOut.ContinuousActions;
        continuousActions[0] = Input.GetAxisRaw("Horizontal");
        continuousActions[1] = Input.GetAxisRaw("Vertical");
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "odun")
        {
            i++;
            AddReward(10f);
            UpdateTotalReward(10f);
        }
        if(other.gameObject.tag =="ates")
        {
            

            if (Envanter.woodCount != 0 && Envanter.camphealthCount>=30)
            {
                AddReward(10f);
                UpdateTotalReward(10f);
                
            }
            if (Envanter.stoneCount != 0 && Envanter.camphealthCount<30)
            {
                AddReward(10f);
                UpdateTotalReward(10f);

            }
        }
        if(other.gameObject.tag =="tas")
        {
            AddReward(10f);
            UpdateTotalReward(10f);
        }
        
        if(other.gameObject.tag =="yemek")
        {
            if(Envanter.hungerCount<30)
            {
                AddReward(10f);
                UpdateTotalReward(10f);
            }
            AddReward(5f);
            UpdateTotalReward(5f);
        }
        
        
    }
    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag == "wall")
        {
            AddReward(-10f);
            UpdateTotalReward(-10f);
        }

    }
    void UpdateTotalReward(float reward)
    {
        totalReward += reward;
        rewardText.text=("Total Reward: " + totalReward.ToString());
    }

    public void Die()
    {

        if (Envanter.healthCount <= 0 || Envanter.camphealthCount <= 0)
        {
            AddReward(-10f);
            UpdateTotalReward(-10f);
            // Tüm envanter öðelerini varsayýlan deðerlere sýfýrla
            Timer.longesTime();
            Envanter.ResetInventory();
            EndEpisode();
            totalReward = 0;
            

        }
    }
    void Update()
    {
        Die();
        if(Mathf.Abs(moveRotate)>0)
        {
            AddReward(-0.01f);
            UpdateTotalReward(-0.01f);
        }
        

    }
    
}
