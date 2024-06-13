using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgents;
using System;
using TMPro;

public class AgentController : Agent//Bu s�n�f, Agent s�n�f�ndan t�retilmi� bir s�n�ft�r. ML-Agents �er�evesindeki bir ajan� temsil eder.
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

    public override void OnEpisodeBegin() //Bu metot, her e�itim b�l�m� (episode) ba�lad���nda �a�r�l�r. Ajan�n ba�lang�� pozisyonunu ve hedef pozisyonunu s�f�rlar.
    {
        transform.localPosition = new Vector3(25.76f, 0.01f, 19.29f);
        

    }
    public override void CollectObservations(VectorSensor sensor)//Bu metot, ajan�n alg�lar�n� (g�zlemlerini) toplar. Burada, ajan�n kendi pozisyonunu ve hedefin pozisyonunu toplar ve VectorSensor kullanarak sensor parametresine ekler.
    {
        sensor.AddObservation(transform.localPosition);
        sensor.AddObservation(target.localPosition);
        sensor.AddObservation(target1.localPosition);
        sensor.AddObservation(target2.localPosition);
    }
    public override void OnActionReceived(ActionBuffers actions)//Bu metot, ajan�n bir eylem ald���nda �a�r�l�r. Burada, ajan�n ald��� eyleme g�re hareket eder.
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

    public override void Heuristic(in ActionBuffers actionsOut)//Bu metot, ajan�n insan taraf�ndan kontrol edildi�i durumlar� sim�le eder. Burada, ajan�n klavye giri�lerine g�re eylemleri belirlenir.
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
            // T�m envanter ��elerini varsay�lan de�erlere s�f�rla
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
