using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.MLAgents;

public class Timer : MonoBehaviour
{
    public static Timer Instance { get; private set; }
    public static float elapsedTime;
    public static float hour = 0;
    public static float day = 0;
    public static float longestTimeLived = 0;
    [SerializeField] private TextMeshProUGUI timerText;
    [SerializeField] private TextMeshProUGUI longestTimeLivedText;
    // Start is called before the first frame update
    void Start()
    {

    }

    private void Awake()
    {
        // Singleton örneðini oluþtur
        if (Instance != null && Instance != this)
        {
            Destroy(this.gameObject);
        }
        else
        {
            Instance = this;
            DontDestroyOnLoad(this.gameObject); // Bu nesneyi sahne deðiþikliklerinde yok etme
        }
    }

    // Update is called once per frame
    void Update()
    {
        elapsedTime += Time.deltaTime;
        int minutes = Mathf.FloorToInt(elapsedTime / 60);
        int seconds = Mathf.FloorToInt(elapsedTime % 60);


        if (hour >= 24)// day passed
        {
            day++;
            hour = 0;

        }
        hour += Time.deltaTime / 1;
        timerText.text = "Day " + day + "(" + (int)hour + "h)";


    }

    public static  void  longesTime()
    {
        if (Instance != null)
        {
            if (day == 0)
            {
                longestTimeLived = elapsedTime;
                Instance.longestTimeLivedText.text = "Best Day: " + "Day " + day + "(" + (int)hour + "h)";
            }
            else
            {
                if (elapsedTime > longestTimeLived)
                {
                    Instance.longestTimeLivedText.text = "Best Day: " + "Day " + day + "(" + (int)hour + "h)";
                    longestTimeLived = elapsedTime;
                }
            }
        }
    }


}
