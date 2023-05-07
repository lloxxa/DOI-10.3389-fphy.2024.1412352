% pillar number, 3C

figure()
hold on
nfiles=670;
cmap=colormap(parula);
integrals= 1:nfiles;
peakstrain=1:nfiles;
for i=1:nfiles
    
    a=importdata(strcat("cup_",int2str(i),"_ret.csv"));
    z=a.data(:,3);
    b=baseline(a.data(:,5), 20);
    f=a.data(:,5)-b;
    
    z_0=z (  find(abs(f(1:500))==min(abs(f(1:500))))  );
    z_0=z_0(1);
    z=z-z_0;
    

    
    
    plot(z, f,'DisplayName', int2str(i), ...
        'Color', colorn(i, nfiles, cmap));
    
    integrals(i)=-integrate(z,f);
    
    % get the baseline
    % find z-value of intersection = point of contact
    % integrate all f < baseline
    grad=gradient(f);
    maxgrad_idx=find(grad==max(grad));
    peakstrain(i)=z(maxgrad_idx(1));
    
end

colorbar();
caxis([1 nfiles]);

f=figure();
histogram(integrals, 100);
savefig(f);

g=figure();
histogram(peakstrain, 100);
savefig(g);

function sum_f=integrate(z,f)
    dz=z(end)/length(f(find(z==0):end));
    sum_f = sum( f(find(z==0):end) ) * dz;
end

function b=baseline(f, ntail)
    b=mean( f( length(f)-ntail:length(f)  ) );
end

% let's go functions
function c=colorn(i, ncolors, cmap)
    n=floor(256/ncolors*i);
    c=cmap(n,:);
end

