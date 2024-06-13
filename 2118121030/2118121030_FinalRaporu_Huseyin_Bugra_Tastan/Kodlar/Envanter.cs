using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Envanter : MonoBehaviour
{

    public static int woodCount = 0;
    public static int stoneCount = 0;
    public static int foodCount = 0;
    public static float healthCount = 100;
    public static float hungerCount = 100;
    public static float camphealthCount = 100;
    [SerializeField] private TextMeshProUGUI woodText;
    [SerializeField] private TextMeshProUGUI stoneText;
    [SerializeField] private TextMeshProUGUI foodText;
    [SerializeField] private TextMeshProUGUI healthText;
    [SerializeField] private TextMeshProUGUI hungerText;
    [SerializeField] private TextMeshProUGUI camphealthText;


    public float decreaseRate = 1f;//de�i�kenin ne kadar azal�ca��
    public float decreaseInterval = 1f;//azalma aral���
    public float addHungerInterval = 30f;
    private float timer = 0f;//zamanl�y�c�
    private float addHungerTimer = 0f;

    

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        foodText.text = foodCount.ToString();
        hungerText.text = hungerCount.ToString();
        woodText.text = woodCount.ToString();
        stoneText.text = stoneCount.ToString();
        healthText.text = healthCount.ToString();
        camphealthText.text = camphealthCount.ToString();



        timer += Time.deltaTime / 2;
        addHungerTimer += Time.deltaTime;
        if (timer >= decreaseInterval)
        {
            hungerCount -= decreaseRate;
            camphealthCount -= decreaseRate;
            timer = 0f;

            if (hungerCount <= 0)
            {
                healthCount -= decreaseRate;

            }
            else // E�er hungerCount 0'dan b�y�kse healthCount azalmayacak
            {
                healthCount = Mathf.Clamp(healthCount, 0, 100);
                healthCount += decreaseRate;
            }
        }
        // Kontrol noktalar� ekleniyor
        if (hungerCount <= 0)
        {
            hungerCount = 0;
            // Burada �rne�in oyun karakterinin �l�m� veya ba�ka bir eylem tetiklenebilir.
        }
        if(hungerCount >= 100)
        {
            hungerCount = 100;
        }

        if (camphealthCount <= 0)
        {
            camphealthCount = 0;
            // Burada �rne�in kamp�n yok olmas� veya ba�ka bir eylem tetiklenebilir.
        }

        //if (hungerCount <= 0 && addHungerTimer >= addHungerInterval)
        //{
           // hungerCount += 10;
           // addHungerTimer = 0f;
        //}
        //if (healthCount <= 0 || camphealthCount <= 0)
        //{
            // T�m envanter ��elerini varsay�lan de�erlere s�f�rla
           // ResetInventory();
            
        //}

    }
    public static void ResetInventory()
    {
        woodCount = 0;
        stoneCount = 0;
        foodCount = 0;
        healthCount = 100;
        hungerCount = 100;
        camphealthCount = 100;
        Timer.day = 0;
        Timer.hour = 0;

        // Karakteri ba�lang�� noktas�na yerle�tir
       // transform.position = spawnPoint;
    }
}
