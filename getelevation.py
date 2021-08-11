import math
import requests

nCONST_NO_DATA = -500

file_pass = "./" # テキストデータ保存用pass

# サブルーチン
def getelevation(lat,long):

    global nCONST_NO_DATA # グローバル定義
    global file_pass

    demSource_list = ['dem5a', 'dem5b', 'dem', 'none'] # データソースリスト
    zoom = [15, 15, 14, 14] # 縮尺
    dataRound = [1, 1, 0, 0] # 小数点以下丸め

    # ラジアンに変換
    lat_rad = math.radians(lat)
    long_rad = math.radians(long)

    R_128 = 128 / math.pi; # 円周率の1/128
    worldCoordX = R_128 * ( long_rad + math.pi ); #専用の計算式(x)
    worldCoordY = ( -1 ) * R_128/2 * math.log( ( 1 + math.sin( lat_rad ) )/( 1 - math.sin( lat_rad ) ) ) + 128 #専用の計算式(x)

    # 取得済みデータ検索
    demSource_use = '' # データ形式を空にする
    i = 0 # カウンタ用
    for demSource in demSource_list:
        PixelX = worldCoordX * pow( 2, zoom[i] )
        TileX = math.floor( PixelX / 256 )
        PixelY = worldCoordY * pow( 2, zoom[i] )
        TileY = math.floor( PixelY / 256 )
        PixelXint = math.floor( PixelX )
        px = PixelXint % 256
        PixelYint = math.floor( PixelY )
        py = PixelYint % 256
        sFileTXT = str(demSource) + "_" + str(TileX) + "_" + str(TileY) + ".txt"
        print(sFileTXT)

        try: # ファイルがあるときの処理
            with open(file_pass + sFileTXT, "r") as sFile:
                sTextAll = sFile.readlines()
                demSource_use = demSource # 使用したデータ形式を保存
                break # ファイルが合ったらforから抜ける

        except: # ファイルが無いときの処理
            pass # ファイルが無いときは何もしない

        i += 1 # カウンタ加算

    if demSource_use == '': # データが無かった時の処理(urlから読み込み)

        i = 0 # カウンタ用
        for demSource in demSource_list:
            PixelX = worldCoordX * pow( 2, zoom[i] )
            TileX = math.floor( PixelX / 256 )
            PixelY = worldCoordY * pow( 2, zoom[i] )
            TileY = math.floor( PixelY / 256 )
            PixelXint = math.floor( PixelX )
            px = PixelXint % 256
            PixelYint = math.floor( PixelY )
            py = PixelYint % 256
            sFileURL = "http://cyberjapandata.gsi.go.jp/xyz/" + str(demSource) + "/" + str(zoom[i]) + "/" + str(TileX) + "/" + str(TileY) + ".txt"
            print(sFileURL) # requests.get実行の確認用

            if demSource == "none": # データが無い座標の時の処理
                demSource_use = demSource
                sFileTXT = str(demSource) + "_" + str(TileX) + "_" + str(TileY) + ".txt"
                with open(file_pass + sFileTXT, "w") as sFile:
                    sFile.write("None")
                
                break

            response = requests.get(sFileURL)

            if response.status_code == 200: # 読み取りに成功した時の処理
                sTextAll = response.text
                demSource_use = demSource # 使用したデータ形式を保存

                # テキストファイルを保存
                sFileTXT = str(demSource) + "_" + str(TileX) + "_" + str(TileY) + ".txt"
                with open(file_pass + sFileTXT, "w") as sFile:
                    sFile.write(sTextAll)
                with open(file_pass + sFileTXT, "r") as sFile:
                    sTextAll = sFile.readlines()

                break # ファイルが合ったらforから抜ける

            i += 1 # カウンタ加算

    if demSource_use == "none": # 範囲外の時の処理
        return None, demSource_use

    # sTextAllが配列になっているのでそのまま使用
    asText = sTextAll
    
    if( len( asText ) < py ):
        return nCONST_NO_DATA
    Lpy = asText[py]
    pxs = Lpy.split(",")
    if( len( pxs ) < px ):
        return nCONST_NO_DATA
    Spx = pxs[px]

    
    if( Spx == "e" ):
        return nCONST_NO_DATA

    Spx = float( Spx )
    Spx = round( Spx, dataRound[i] )

    if( Spx <- 500 ):
        Spx = None

    return Spx, demSource_use
  

if __name__ == '__main__':
    print(getelevation(36.103543, 140.08531))
