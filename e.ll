define void @E_(half* noalias %data0,i16* noalias %data1) {
  %v0 = getelementptr inbounds i16, i16* %data1, i32 0
  %v1 = load i16, i16* %v0
  %v2 = zext i16 %v1 to i32
  %v3 = getelementptr inbounds half, half* %data0, i32 0
  %v4 = mul i32 %v2, 65536
  %v5 = bitcast i32 %v4 to float
  %v6 = fptrunc float %v5 to half
  store half %v6, half* %v3
  ret void
}